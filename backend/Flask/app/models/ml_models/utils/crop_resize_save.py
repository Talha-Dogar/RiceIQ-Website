import cv2
import numpy as np
import uuid
import os
from typing import List, Dict, Union, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class GrainProcessor:
    def __init__(self, 
                 target_height: int = 224, 
                 target_width: int = 224,
                 min_area: int = 100, 
                 padding: int = 5,
                 max_workers: Optional[int] = None,
                 storage_path: str = None):
        """
        Initialize grain processor with advanced memory management and file storage
        
        Args:
            target_height (int): Target height for resized grains
            target_width (int): Target width for resized grains
            min_area (int): Minimum contour area to filter grains
            padding (int): Pixel padding around each grain
            max_workers (int, optional): Maximum threads for parallel processing
            storage_path (str, optional): Path to store resized grain images
        """
        self.target_height = target_height
        self.target_width = target_width
        self.min_area = min_area
        self.padding = padding
        self.max_workers = max_workers or (os.cpu_count() or 1)
        
        # Set default storage path if not provided
        self.storage_path = storage_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'single_grains')
        
        # Ensure storage directory exists
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Memory storage for grains
        self.memory_storage: Dict[str, np.ndarray] = {}
        
        # Thread-safe storage
        self._thread_local = threading.local()

    def resize_image_preserve_features(
        self, 
        image: np.ndarray, 
        target_height: Optional[int] = None, 
        target_width: Optional[int] = None
    ) -> np.ndarray:
        """
        Resize image while preserving key features
        
        Args:
            image (np.ndarray): Input image
            target_height (int, optional): Override default target height
            target_width (int, optional): Override default target width
        
        Returns:
            np.ndarray: Preprocessed image
        """
        # Use class defaults if not specified
        th = target_height or self.target_height
        tw = target_width or self.target_width
        
        # Ensure image is 3-channel
        if len(image.shape) < 3:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        
        # Get the image dimensions
        h, w = image.shape[:2]
        
        # Choose interpolation method based on resize direction
        interpolation = (cv2.INTER_AREA if h > th or w > tw 
                         else cv2.INTER_CUBIC)
        
        # Calculate aspect ratio resize
        aspect_ratio = w / h
        
        if aspect_ratio > 1:  # landscape
            new_width = tw
            new_height = int(new_width / aspect_ratio)
        else:  # portrait or square
            new_height = th
            new_width = int(new_height * aspect_ratio)
        
        # Resize while maintaining aspect ratio
        resized_image = cv2.resize(image, (new_width, new_height), 
                                   interpolation=interpolation)
        
        # Create black canvas
        final_image = np.zeros((th, tw, 3), dtype=np.uint8)
        
        # Center the resized image
        y_offset = (th - new_height) // 2
        x_offset = (tw - new_width) // 2
        
        final_image[y_offset:y_offset+new_height, 
                    x_offset:x_offset+new_width] = resized_image
        
        # Sharpening filter
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        sharpened_image = cv2.filter2D(final_image, -1, kernel)
        
        # Blend original and sharpened
        final_image = cv2.addWeighted(final_image, 0.7, 
                                      sharpened_image, 0.3, 0)
        
        return final_image
    def process_single_image(self, image_path: str) -> List[str]:
        """
        Process a single image to extract and store grains with original appearance
        and black background.
        
        Args:
            image_path (str): Path to input image
        
        Returns:
            List of unique grain identifiers
        """
        # Load image
        image = cv2.imread(image_path)
        
        # Convert to grayscale for thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) > 2 else image
        
        # Apply thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.min_area]
        
        # Store grains
        grain_ids = []
        for contour in valid_contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Add padding
            x = max(0, x - self.padding)
            y = max(0, y - self.padding)
            w = min(image.shape[1] - x, w + 2*self.padding)
            h = min(image.shape[0] - y, h + 2*self.padding)
            
            # Create mask for this contour area
            mask = np.zeros((y+h-y, x+w-x, 3), dtype=np.uint8)
            cv2.drawContours(mask, [contour], 0, (1, 1, 1), -1, offset=(-x, -y))
            
            # Crop the grain from original image
            grain_region = image[y:y+h, x:x+w]
            
            # Apply mask to keep original grain appearance with black background
            masked_grain = grain_region * mask
            
            # Generate unique ID
            grain_id = f'grain_{uuid.uuid4()}'
            
            # Store in memory
            self.memory_storage[grain_id] = masked_grain
            grain_ids.append(grain_id)
        
        return grain_ids

    def process_images(self, image_paths: List[str]) -> Dict[str, List[str]]:
        """
        Process multiple images sequentially
        
        Args:
            image_paths (List[str]): List of image paths to process
        
        Returns:
            Dictionary mapping image paths to their grain identifiers
        """
        # Dictionary to store results
        batch_results: Dict[str, List[str]] = {}
        
        # Process images sequentially
        for image_path in image_paths:
            try:
                grain_ids = self.process_single_image(image_path)
                batch_results[image_path] = grain_ids
            except Exception as exc:
                print(f"Error processing {image_path}: {exc}")
        
        return batch_results

    def _save_grain_to_file(self, grain_id: str, image: np.ndarray) -> str:
        """
        Save grain image to file
        
        Args:
            grain_id (str): Unique grain identifier
            image (np.ndarray): Grain image to save
            
        Returns:
            str: File path where the grain was saved
        """
        # Create a valid filename from the grain ID
        filename = f"{grain_id}.png"
        file_path = os.path.join(self.storage_path, filename)
        
        # Save the image
        cv2.imwrite(file_path, image)
        
        return file_path

    def batch_resize_grains(
        self, 
        grain_ids: Optional[List[str]] = None,
        target_height: Optional[int] = None,
        target_width: Optional[int] = None,
        save_to_disk: bool = True,
        return_paths_only: bool = False
    ) -> Union[Dict[str, np.ndarray], Dict[str, str]]:
        """
        Batch resize stored grains and optionally save to disk
        
        Args:
            grain_ids (List[str], optional): Specific grains to resize. 
                                             If None, resizes all stored grains.
            target_height (int, optional): Override default target height
            target_width (int, optional): Override default target width
            save_to_disk (bool): Whether to save resized grains to disk
            return_paths_only (bool): If True, return only file paths instead of images
        
        Returns:
            If return_paths_only is False: Dictionary of resized grains (grain_id -> np.ndarray)
            If return_paths_only is True: Dictionary of file paths (grain_id -> file_path)
        """
        # Use all stored grains if no specific IDs provided
        if grain_ids is None:
            grain_ids = list(self.memory_storage.keys())
        
        # Resize grains
        resized_grains: Dict[str, np.ndarray] = {}
        file_paths: Dict[str, str] = {}
        
        # Use ThreadPoolExecutor for concurrent resizing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit resizing tasks
            future_to_grain = {
                executor.submit(
                    self.resize_image_preserve_features, 
                    self.memory_storage[grain_id],
                    target_height,
                    target_width
                ): grain_id for grain_id in grain_ids
            }
            
            # Collect results
            for future in as_completed(future_to_grain):
                grain_id = future_to_grain[future]
                try:
                    resized_grain = future.result()
                    
                    # Always save to disk if return_paths_only is True
                    if save_to_disk or return_paths_only:
                        file_path = self._save_grain_to_file(grain_id, resized_grain)
                        file_paths[grain_id] = file_path
                    
                    # Only store in memory if not return_paths_only
                    if not return_paths_only:
                        resized_grains[grain_id] = resized_grain
                        
                except Exception as exc:
                    print(f"Error resizing grain {grain_id}: {exc}")
        
        # Store file paths in memory for reference
        self._file_paths = file_paths
        
        # Return based on flag
        if return_paths_only:
            return file_paths
        else:
            return resized_grains

    def load_grain_from_path(self, file_path: str) -> np.ndarray:
        """
        Load a grain image from file path
        
        Args:
            file_path (str): Path to the grain image file
            
        Returns:
            np.ndarray: Loaded image
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Grain image not found at {file_path}")
            
        # Read image using OpenCV
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Failed to load image from {file_path}")
            
        return image

    def clear_memory(self, grain_ids: Optional[List[str]] = None, delete_files: bool = False):
        """
        Clear memory storage and optionally delete saved files
        
        Args:
            grain_ids (List[str], optional): Specific grains to remove. 
                                             If None, clears all stored grains.
            delete_files (bool): Whether to delete corresponding files
        """
        file_paths = getattr(self, '_file_paths', {})
        
        if grain_ids is None:
            # Clear entire memory storage
            grain_ids = list(self.memory_storage.keys())
            self.memory_storage.clear()
            
            # Delete all files if requested
            if delete_files:
                for grain_id, file_path in file_paths.items():
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
                self._file_paths = {}
        else:
            # Remove specific grains
            for grain_id in grain_ids:
                self.memory_storage.pop(grain_id, None)
                
                # Delete file if requested
                if delete_files and grain_id in file_paths:
                    file_path = file_paths[grain_id]
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        file_paths.pop(grain_id, None)
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
                        
    def cleanup_storage_directory(self):
        """
        Clean up the entire storage directory
        
        This will remove all files in the storage directory but keep the directory itself
        """
        try:
            # Check if directory exists
            if os.path.exists(self.storage_path) and os.path.isdir(self.storage_path):
                # Get all files in the directory
                for filename in os.listdir(self.storage_path):
                    file_path = os.path.join(self.storage_path, filename)
                    # Remove if it's a file
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                
                print(f"Cleaned up all files in {self.storage_path}")
                # Clear file paths record
                self._file_paths = {}
                return True
            else:
                print(f"Storage directory {self.storage_path} does not exist")
                return False
        except Exception as e:
            print(f"Error cleaning up storage directory: {e}")
            return False