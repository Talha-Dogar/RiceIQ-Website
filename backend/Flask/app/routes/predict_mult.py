import threading
from flask import Blueprint, request, jsonify
import tensorflow as tf
from datetime import datetime
# from werkzeug.utils import secure_filename
import os
import numpy as np
from flask import request, jsonify
from ..models.sample_result import insert_sample_and_result
from ..models.ml_models.mobilenet import load
from ..models.ml_models.mobilenet import predict_image
from ..models.ml_models.utils.preprocess_MobileNet import load_and_preprocess_image, preprocess_image
from ..models.ml_models.efficient import load_E
from ..models.ml_models.utils.preprocess_EfficientNet import load_and_preprocess_image_E, preprocess_image_E
from ..models.ml_models.efficient import predict_image_E
from ..models.ml_models.utils.conf_gpu import configure_gpu
# from ..models.ml_models.utils.crop import GrainProcessor
from ..models.ml_models.utils.crop_resize import GrainProcessor
predictmul_bp = Blueprint('predictmul', __name__)
def get_current_datetime_iso():
    return datetime.now().replace(microsecond=0).isoformat()


configure_gpu()
# Load models globally
mobilenet_model = load("/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/final_best_model.keras")
efficientnet_model = load_E("/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/efficientnet.keras")
processor = GrainProcessor(
        target_height=224,
        target_width=224,
        min_area=100,
        padding=5
    )


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
            print("\n\n",type(grain_image), "\n\n\n")
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

def predict_grains_batch(model, processed_batch, riceVarieties, threshold=0.35):
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


# Modified predict route
@predictmul_bp.route('/predictmul', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        riceVarieties = {
            0: '1509', 1: 'Basmati-2000', 2: 'IR-6', 3: 'PK-1121',
            4: 'PK-386', 5: 'Sela', 6: 'SuperBasmati', 7: 'Supri'
        }

        upload_folder = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Process grains
        batch_results = processor.process_images([file_path])
        all_grain_ids = [
            grain_id 
            for grain_ids in batch_results.values() 
            for grain_id in grain_ids
        ]
        resized_grains = processor.batch_resize_grains(grain_ids=all_grain_ids)

        # Predict using both models in parallel
        results = {}

        def predict_model(model, model_name):
            with tf.device('/GPU:0'):
                # Process grains for the specific model
                processed_batch, processed_grain_ids = process_grains_for_prediction(
                    resized_grains, 
                    model_type='mobilenet' if model_name == 'mobilenet' else 'efficientnet'
                )
                
                # Batch prediction
                batch_predictions = predict_grains_batch(
                    model, processed_batch, riceVarieties
                )
                
                # Combine predictions with grain IDs
                detailed_results = [
                    {**pred, 'grain_id': grain_id} 
                    for pred, grain_id in zip(batch_predictions, processed_grain_ids)
                ]
                
                results[model_name] = detailed_results

        # Create threads for parallel prediction
        t1 = threading.Thread(target=predict_model, args=(mobilenet_model, 'mobilenet'))
        t2 = threading.Thread(target=predict_model, args=(efficientnet_model, 'efficientnet'))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Aggregate and choose final prediction
        # You can implement more sophisticated aggregation logic here
        final_predictions = results['efficientnet']  # or merge/compare results

        # Prepare result data
        sample_data = {
            "imgUrl": file_path,
            "createdAt": get_current_datetime_iso()
        }

        result_data = {
            "confidenceScore": f"{final_predictions[0]['confidence']:.2%}",
            "varietyNames": [pred['variety'] for pred in final_predictions],
            "adulterationStatus": "False",
            "percentageComposition": {
                pred['variety']: f"{pred['confidence']:.2%}" 
                for pred in final_predictions
            },
            "obtainAt": get_current_datetime_iso()
        }

        # result_id = insert_sample_and_result(sample_data, result_data)
        # print("prediction", type(final_predictions))
        return jsonify({
            'resultID': str(123),
            # 'predictions': final_predictions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
