from PIL import Image
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image

def load_and_preprocess_image_E(image_path, target_size=(224, 224)):
    # Load image with PIL
    img = Image.open(image_path)
    
    # Resize image
    img = img.resize(target_size)
    
    # Convert PIL image to numpy array
    img_array = np.array(img)
    
    # Apply MobileNetV3 preprocessing
    img_array = preprocess_input(img_array)
    
    # Add batch dimension for inference
    # img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def preprocess_image_E(img_path):
    img = image.load_img(img_path)
    img_array = image.img_to_array(img)
    # img_array = np.array(image)
    
    # Apply MobileNetV3 preprocessing
    img_array = preprocess_input(img_array)
    
    # Add batch dimension for inference
    # img_array = np.expand_dims(img_array, axis=0)
    
    return img_array