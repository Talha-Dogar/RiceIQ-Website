import numpy as np
import tensorflow as tf

def process_grains_for_prediction(resized_grains, model_type='mobilenet'):
    """
    Process resized grain images for model prediction.
    
    Args:
        resized_grains (dict): Dictionary of resized grain images
        model_type (str): Type of model ('mobilenet' or 'efficientnet')
    
    Returns:
        tuple: Processed images batch and corresponding grain IDs
    """
    processed_images = []
    processed_grain_ids = []
    
    for grain_id, grain_image in resized_grains.items():
        try:
            # Preprocess image based on model type
            if model_type == 'mobilenet':
                processed_img = preprocess_image(grain_image)
            elif model_type == 'efficientnet':
                processed_img = preprocess_image_E(grain_image)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            processed_images.append(processed_img)
            processed_grain_ids.append(grain_id)
        
        except Exception as e:
            print(f"Error processing grain {grain_id}: {e}")
    
    # Convert to numpy array if needed
    processed_batch = np.array(processed_images)
    
    return processed_batch, processed_grain_ids

def predict_grains_batch(model, processed_batch, riceVarieties, threshold=0.5):
    """
    Predict rice varieties for a batch of processed grain images.
    
    Args:
        model: Loaded TensorFlow model
        processed_batch (np.array): Batch of preprocessed images
        riceVarieties (dict): Mapping of model output indices to variety names
        threshold (float): Confidence threshold for prediction
    
    Returns:
        list: Predictions for each grain with variety and confidence
    """
    # Batch prediction
    predictions = model.predict(processed_batch)
    
    batch_results = []
    for pred in predictions:
        predicted_class = np.argmax(pred)
        confidence = pred[predicted_class]
        
        # Apply confidence threshold
        if confidence >= threshold:
            variety = riceVarieties.get(predicted_class, 'Unknown')
            batch_results.append({
                'variety': variety,
                'confidence': float(confidence),
                'predicted_class': predicted_class
            })
        else:
            batch_results.append({
                'variety': 'Uncertain',
                'confidence': float(confidence),
                'predicted_class': predicted_class
            })
    
    return batch_results
