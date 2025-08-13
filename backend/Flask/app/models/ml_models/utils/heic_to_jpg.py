import pyheif
from PIL import Image
import os

def convert_heic_to_jpg(input_path, output_path=None):
    # Read HEIC file
    heif_file = pyheif.read(input_path)
    
    # Convert to PIL Image
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Generate output path if not given
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".jpg"
    
    # Save as JPG
    image.save(output_path, format="JPEG")
    return output_path
    # print(f"Saved JPG to: {output_path}")

# Example usage
