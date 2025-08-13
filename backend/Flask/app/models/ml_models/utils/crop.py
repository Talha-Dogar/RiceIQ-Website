import os
import cv2
import numpy as np
import uuid
import tempfile
from typing import List, Dict, Union
import boto3  # Optional, for cloud storage
import redis  # Optional, for caching

class GrainProcessor:
    def __init__(self, 
                 storage_method: str = 'local', 
                 storage_path: str = 'cropped_grains',
                 cloud_bucket: str = None):
        """
        Initialize grain processing with configurable storage options.
        
        Args:
            storage_method (str): Storage method - 'local', 'memory', or 'cloud'
            storage_path (str): Local directory for storing cropped grains
            cloud_bucket (str, optional): S3 bucket name for cloud storage
        """
        self.storage_method = storage_method
        self.storage_path = storage_path
        self.cloud_bucket = cloud_bucket
        
        # Create local storage directory if needed
        if storage_method == 'local':
            os.makedirs(storage_path, exist_ok=True)
        
        # Optional cloud storage setup
        if storage_method == 'cloud':
            self.s3_client = boto3.client('s3')
        
        # Optional in-memory storage
        self.memory_storage: Dict[str, np.ndarray] = {}

    def process_grains(self, image_path: str, min_area: int = 100, padding: int = 5) -> List[Union[str, np.ndarray]]:
        """
        Process grains in an image and store/return them based on storage method.
        
        Args:
            image_path (str): Path to the input image
            min_area (int): Minimum contour area to consider as a valid grain
            padding (int): Pixel padding around each grain
        
        Returns:
            List of grain identifiers or numpy arrays depending on storage method
        """
        # Load and preprocess image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) > 2 else image
        
        # Apply thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        # Find and filter contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        # Process and store grains
        processed_grains = []
        for i, contour in enumerate(valid_contours):
            # Get bounding rectangle with padding
            x, y, w, h = cv2.boundingRect(contour)
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2*padding)
            h = min(image.shape[0] - y, h + 2*padding)
            
            # Crop the grain
            grain = image[y:y+h, x:x+w]
            
            # Store based on method
            if self.storage_method == 'local':
                # Generate unique filename
                filename = os.path.join(self.storage_path, f'grain_{uuid.uuid4()}.jpg')
                cv2.imwrite(filename, grain)
                processed_grains.append(filename)
            
            elif self.storage_method == 'memory':
                # Store in memory with unique key
                grain_id = f'grain_{uuid.uuid4()}'
                self.memory_storage[grain_id] = grain
                processed_grains.append(grain_id)
            
            elif self.storage_method == 'cloud':
                # Upload to S3
                if not self.cloud_bucket:
                    raise ValueError("Cloud bucket not specified")
                
                # Create a temporary file to upload
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    cv2.imwrite(temp_file.name, grain)
                    grain_id = f'grain_{uuid.uuid4()}.jpg'
                    
                    # Upload to S3
                    self.s3_client.upload_file(
                        temp_file.name, 
                        self.cloud_bucket, 
                        grain_id
                    )
                    
                    # Remove temporary file
                    os.unlink(temp_file.name)
                    
                    processed_grains.append(grain_id)
        
        return processed_grains

    def retrieve_grain(self, grain_identifier: str) -> np.ndarray:
        """
        Retrieve a previously processed grain.
        
        Args:
            grain_identifier: Unique identifier of the grain
        
        Returns:
            Numpy array of the grain image
        """
        if self.storage_method == 'local':
            return cv2.imread(grain_identifier)
        
        elif self.storage_method == 'memory':
            return self.memory_storage.get(grain_identifier)
        
        elif self.storage_method == 'cloud':
            # Download from S3
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                self.s3_client.download_file(
                    self.cloud_bucket, 
                    grain_identifier, 
                    temp_file.name
                )
                grain = cv2.imread(temp_file.name)
                os.unlink(temp_file.name)
                return grain
        
        raise ValueError("Invalid storage method")

# # Example usage
# def main():
#     # Local storage example
#     local_processor = GrainProcessor(storage_method='local')
#     local_grains = local_processor.process_grains('/path/to/image.jpg')
    
#     # Memory storage example
#     memory_processor = GrainProcessor(storage_method='memory')
#     memory_grains = memory_processor.process_grains('/path/to/image.jpg')
    
#     # Cloud storage example (requires AWS credentials and S3 bucket)
#     # cloud_processor = GrainProcessor(
#     #     storage_method='cloud', 
#     #     cloud_bucket='your-s3-bucket-name'
#     # )
#     # cloud_grains = cloud_processor.process_grains('/path/to/image.jpg')

# if __name__ == '__main__':
#     main()