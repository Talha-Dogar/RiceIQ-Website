import threading
from flask import Blueprint, request, jsonify
import tensorflow as tf
from datetime import datetime
import os
import numpy as np
import shutil
from flask import request, jsonify
from ..models.sample_result import insert_sample_and_result
from ..models.ml_models.mobilenet import load
from ..models.ml_models.mobilenet import predict_image
from ..models.ml_models.utils.preprocess_MobileNet import load_and_preprocess_image, preprocess_image
from ..models.ml_models.efficient import load_E
from ..models.ml_models.utils.preprocess_EfficientNet import load_and_preprocess_image_E, preprocess_image_E
from ..models.ml_models.efficient import predict_image_E
from ..models.ml_models.inception import load_I, predict_image_I
from ..models.ml_models.utils.preprocess_inception import preprocess_image_I
from ..models.ml_models.densenet import load_D
from ..models.ml_models.utils.preprocess_densenet import preprocess_image_D
from ..models.ml_models.utils.conf_gpu import configure_gpu
from ..models.ml_models.utils.crop_resize_save import GrainProcessor

predictmul_v2_bp = Blueprint('predictmul_v2', __name__)

def get_current_datetime_iso():
    return datetime.now().replace(microsecond=0).isoformat()

# Define path for single grains storage
SINGLE_GRAINS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  '..', 'models', 'ml_models', 'utils', 'single_grains')

# Make sure the directory exists
os.makedirs(SINGLE_GRAINS_PATH, exist_ok=True)

configure_gpu()
# Load models globally
mobilenet_model = load("/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/final_best_model.keras")
efficientnet_model = load_E("/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/efficientnet.keras")
inception_model = load_I("/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/inception.keras")
densenet_model = load_D("/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/DenseNetV7_4000(90Layers).keras")
processor = GrainProcessor(
    target_height=224,
    target_width=224,
    min_area=100,
    padding=5,
    storage_path=SINGLE_GRAINS_PATH
)

def process_grains_for_prediction(grain_paths, model_type='mobilenet'):
    """
    Process grain images loaded from file paths for model prediction.
    
    Args:
        grain_paths (dict): Dictionary of grain_id -> file_path
        model_type (str): Type of model ('mobilenet' or 'efficientnet')
    
    Returns:
        tuple: Processed images batch and corresponding grain IDs
    """
    processed_images = []
    processed_grain_ids = []
    
    for grain_id, file_path in grain_paths.items():
        try:
            # Load image from file
            # grain_image = cv2.imread(file_path)
            # if grain_image is None:
            #     print(f"Failed to load image at {file_path}")
            #     continue
                
            # Preprocess image based on model type
            if model_type == 'mobilenet':
                processed_img = preprocess_image(file_path)
            elif model_type == 'efficientnet':
                processed_img = preprocess_image_E(file_path)
            elif model_type == 'inception':
                processed_img = preprocess_image_I(file_path)
            elif model_type == 'densenet':
                processed_img = preprocess_image_D(file_path)
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
@predictmul_v2_bp.route('/predictmul_v2', methods=['POST'])
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

        # Make sure storage directory is clean before processing
        processor.cleanup_storage_directory()
        
        # Process grains
        batch_results = processor.process_images([file_path])
        all_grain_ids = [
            grain_id 
            for grain_ids in batch_results.values() 
            for grain_id in grain_ids
        ]
        
        # Save grains to disk and get the file paths instead of images
        grain_file_paths = processor.batch_resize_grains(
            grain_ids=all_grain_ids,
            save_to_disk=True,
            return_paths_only=True
        )

        # Predict using both models in parallel
        results = {}

        def predict_model(model, model_name):
            with tf.device('/GPU:0'):
                # Process grains for the specific model using file paths
                processed_batch, processed_grain_ids = process_grains_for_prediction(
                    grain_file_paths, 
                    model_type='mobilenet' if model_name == 'mobilenet' else 'inception' if model_name == "inception" else 'efficientnet' if model_name == "efficientnet" else 'densenet'
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
        t3 = threading.Thread(target=predict_model, args=(inception_model, 'inception'))
        t4 = threading.Thread(target=predict_model, args=(densenet_model, 'densenet'))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()

        # Aggregate and choose final prediction
        # You can implement more sophisticated aggregation logic here
        final_predictions = results['densenet'] 
        for model_name in ['mobilenet', 'efficientnet', 'inception', 'densenet']:
            print(f"\n\nResults from {model_name}:\n")
            predictions = results[model_name]
            for pred in predictions:
                print(f"{pred['variety']}: {pred['confidence']:.2%}")


         # or merge/compare results

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
        # print("\n\n\n result\n\n", result_data)
        # Clean up the grain files before sending response
        # processor.cleanup_storage_directory()
        
        # result_id = insert_sample_and_result(sample_data, result_data)
        # print("prediction", type(final_predictions))
        return jsonify({
            'resultID': str(123),
            # 'predictions': final_predictions
        })

    except Exception as e:
        # Make sure to clean up in case of error
        try:
            processor.cleanup_storage_directory()
        except:
            pass
        return jsonify({'error': str(e)}), 500