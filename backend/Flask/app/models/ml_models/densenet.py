import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model


def load_D(saved_model_path):
    inference_model=load_model(saved_model_path,compile=False)
    return inference_model
    

def predict_Image_D(model, preprocessed_image, class_list):
    """
    Predict the class of an image using the provided model.
    
    Args:
        model: Loaded MobileNetV3 model
        preprocessed_image: Image preprocessed with MobileNetV3 preprocessing
        class_list: List of class names
    
    Returns:
        tuple: (predicted_class_name, confidence_score)
    """
    # Make prediction
    print("predicting inception..... \n\n")
    predictions = model.predict(preprocessed_image)
    print(predictions)
    # Get the index of the highest confidence prediction
    predicted_class_index = np.argmax(predictions[0])
    
    # Get the confidence score (probability)
    confidence_score = float(predictions[0][predicted_class_index])
    
    # Get the class name from the class list
    predicted_class_name = class_list[predicted_class_index]
    
    return predicted_class_name, confidence_score