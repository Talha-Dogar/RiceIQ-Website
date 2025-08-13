import threading
from flask import Blueprint, request, jsonify
import tensorflow as tf
from datetime import datetime
import os
import numpy as np
import shutil
from ..models.sample_result import insert_sample_and_result
from ..models.sample_result import insert_sample_and_identification_result
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
from ..models.ml_models.utils.heic_to_jpg import convert_heic_to_jpg


predictmul_v3_bp = Blueprint('predict/identification',__name__)

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

def predict_grains_batch(model, processed_batch, riceVarieties, threshold=0.001):
    """
    Predict rice varieties for a batch of processed grain images.
    
    Args:
        model: Loaded TensorFlow model
        processed_batch (np.array): Batch of preprocessed images
        riceVarieties (dict): Mapping of model output indices to variety names
        threshold (float): Confidence threshold for prediction
    
    Returns:
        list: Raw prediction probabilities and derived results for each grain
    """
    # Batch prediction - this returns the raw probability vectors directly from the model
    predictions = model.predict(processed_batch)
    
    batch_results = []
    for pred in predictions:
        # Get the highest probability class and its confidence 
        predicted_class = np.argmax(pred)
        confidence = pred[predicted_class]
        
        # Store the raw predictions vector and derived results
        result = {
            'predicted_class': int(predicted_class),
            'confidence': float(confidence),
            'variety': riceVarieties.get(predicted_class, 'Unknown'),
            'raw_predictions': pred.tolist()  # The full prediction vector with probabilities for all classes
        }
        batch_results.append(result)
    
    return batch_results, predictions  # Return both processed results and raw prediction vectors

def ensemble_predictions(model_predictions, grain_ids, riceVarieties, threshold=0.35):
    """
    Ensemble predictions from multiple models by averaging raw prediction vectors.
    
    Args:
        model_predictions (dict): Dictionary with model names as keys and raw prediction arrays as values
        grain_ids (list): List of grain IDs corresponding to the predictions
        riceVarieties (dict): Mapping of model output indices to variety names
        threshold (float): Confidence threshold for prediction
    
    Returns:
        list: Ensemble predictions for each grain
    """
    if not model_predictions or not grain_ids:
        return []
    
    # Get the number of samples and classes from the first model's predictions
    first_model = list(model_predictions.values())[0]
    num_samples = first_model.shape[0]
    num_classes = first_model.shape[1]
    
    # Organize predictions by sample index
    ensemble_results = []
    
    # For each grain/sample
    for i in range(num_samples):
        grain_id = grain_ids[i]
        
        # Initialize array for summing prediction vectors
        ensemble_pred_vector = np.zeros(num_classes)
        model_count = 0
        
        # Add the predictions from each model for this sample
        for model_name, predictions in model_predictions.items():
            if i < len(predictions):  # Ensure index is valid
                ensemble_pred_vector += predictions[i]
                model_count += 1
        
        # Average the predictions
        if model_count > 0:
            ensemble_pred_vector /= model_count
        
        # Get the predicted class and confidence from the ensemble vector
        predicted_class = np.argmax(ensemble_pred_vector)
        confidence = float(ensemble_pred_vector[predicted_class])
        
        # Create ensemble result
        ensemble_result = {
            'grain_id': grain_id,
            'predicted_class': int(predicted_class),
            'confidence': confidence,
            'variety': riceVarieties.get(predicted_class, 'Unknown'),
            'ensemble_predictions': ensemble_pred_vector.tolist()
        }
        ensemble_results.append(ensemble_result)
    
    return ensemble_results, num_samples

# Modified predict route
@predictmul_v3_bp.route('/predict/identification', methods=['POST'])
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
    # Check if image is HEIC format and convert if needed
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.heic', '.heif']:
            print(f"Converting HEIC image: {file_path}")
            jpg_path = os.path.splitext(file_path)[0] + ".jpg"
            file_path = convert_heic_to_jpg(file_path, jpg_path)
            print(f"Converted to JPG: {file_path}")


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

        # Predict using all models in parallel
        processed_results = {}
        raw_predictions = {}  # Store raw probability vectors directly from models
        grain_id_mapping = {}  # Store grain IDs corresponding to predictions
        lock = threading.Lock()  # For thread-safe access to shared resources

        def predict_model(model, model_name):
            with tf.device('/GPU:0'):
                # Process grains for the specific model using file paths
                model_type = {
                    'mobilenet': 'mobilenet',
                    'efficientnet': 'efficientnet',
                    'inception': 'inception',
                    'densenet': 'densenet'
                }.get(model_name, 'mobilenet')
                
                processed_batch, processed_grain_ids = process_grains_for_prediction(
                    grain_file_paths, model_type=model_type
                )
                
                # Batch prediction - get both processed results and raw prediction vectors
                batch_results, model_raw_predictions = predict_grains_batch(
                    model, processed_batch, riceVarieties
                )
                
                # Combine processed results with grain IDs
                detailed_results = [
                    {**pred, 'grain_id': grain_id} 
                    for pred, grain_id in zip(batch_results, processed_grain_ids)
                ]
                
                # Thread-safe update of results
                with lock:
                    processed_results[model_name] = detailed_results
                    raw_predictions[model_name] = model_raw_predictions
                    if model_name == 'mobilenet':  # Use mobilenet's grain mapping for consistency
                        grain_id_mapping[model_name] = processed_grain_ids

        # Create threads for parallel prediction
        threads = [
            threading.Thread(target=predict_model, args=(mobilenet_model, 'mobilenet')),
            threading.Thread(target=predict_model, args=(efficientnet_model, 'efficientnet')),
            threading.Thread(target=predict_model, args=(inception_model, 'inception')),
            threading.Thread(target=predict_model, args=(densenet_model, 'densenet'))
        ]

        # Start and join all threads
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Print results from each model
        for model_name in processed_results:
            print(f"\n\nResults from {model_name}:\n")
            predictions = processed_results[model_name]
            for pred in predictions:
                print(f"{pred['variety']}: {pred['confidence']:.2%}")

        # Calculate ensemble predictions using the raw probability vectors
        # Use mobilenet's grain_ids for ensembling (assuming same order of grains across models)
        final_predictions, num_grains = ensemble_predictions(
            raw_predictions, 
            grain_id_mapping.get('mobilenet', []), 
            riceVarieties
        )
        
        # print("\n\nEnsemble Results:\n")
        # max_confidence = 0
        # best_variety = ""

        # for pred in final_predictions:
        #     confidence = pred['confidence']
        #     variety = pred['variety']
        #     print(f"{variety}: {confidence:.2%}")
            
        #     if confidence > max_confidence:
        #         max_confidence = confidence
        #         best_variety = variety

        print("\n\nEnsemble Results:\n")
        max_confidence = 0
        best_variety = ""

        # Initialize tracking dictionaries for variety frequencies and confidence sums
        variety_frequencies = {}
        variety_confidence_sums = {}
        confidence_to_return = {}
        
        # Process final predictions to track variety frequencies and confidence sums
        for pred in final_predictions:
            variety = pred['variety']

            confidence = pred['confidence']
            print(f"{variety}: {confidence:.2%}")
            
            # Track frequency of each variety
            if variety in variety_frequencies:
                variety_frequencies[variety] += 1
            else:
                variety_frequencies[variety] = 1
                
            # Track sum of confidence scores for each variety
            if variety in variety_confidence_sums:
                variety_confidence_sums[variety] += confidence
            else:
                variety_confidence_sums[variety] = confidence

            if variety in confidence_to_return:
                if confidence_to_return[variety] < confidence:
                    confidence_to_return[variety] = confidence
            else:
                    confidence_to_return[variety] = confidence

            
        
        # Calculate average confidence for each variety
        variety_avg_confidence = {}
        for variety, total_confidence in variety_confidence_sums.items():
            if variety_frequencies[variety] > 0:  # Avoid division by zero
                variety_avg_confidence[variety] = total_confidence / variety_frequencies[variety]
            else:
                variety_avg_confidence[variety] = 0
                
        # Find maximum frequency
        max_freq = 0
        if variety_frequencies:
            max_freq = max(variety_frequencies.values())
            
        # Find all varieties with maximum frequency
        max_freq_varieties = [v for v, freq in variety_frequencies.items() if freq == max_freq]
        
        # Determine best variety based on frequency and average confidence
        if max_freq_varieties:
            if len(max_freq_varieties) == 1:
                # Only one variety with max frequency
                best_variety = max_freq_varieties[0]
                max_confidence = variety_avg_confidence[best_variety]
            else:
                # Multiple varieties with max frequency, use average confidence as tiebreaker
                best_variety = max(max_freq_varieties, key=lambda v: variety_confidence_sums[v])
                max_confidence = variety_avg_confidence[best_variety]
                
        # # Print variety frequencies and confidence sums/averages
        # print("\n\nVariety Frequencies:")
        # for variety, count in variety_frequencies.items():
        #     print(f"{variety}: {count} grains")
            
        # print("\n\nVariety Confidence Sums:")
        # for variety, conf_sum in variety_confidence_sums.items():
        #     print(f"{variety}: {conf_sum:.4f}")
            
        # print("\n\nVariety Average Confidence:")
        # for variety, avg_conf in variety_avg_confidence.items():
        #     print(f"{variety}: {avg_conf:.4f}")

        status = request.form.get('status', 'pending')  # Default to 'pending' if not provided
        # Prepare result data
        sample_data = {
            "imgUrl": file_path,
            "status": status,
            "createdAt": get_current_datetime_iso()
        }


        # Prepare result data with ensemble predictions
        result_data = {
            # "confidenceScore": f"{final_predictions[0]['confidence']:.2%}" if final_predictions else "0%",
            "confidenceScore": str(confidence_to_return[best_variety])+"%",
            "varietyName": best_variety,
            "total_grains": num_grains,
            # "percentageComposition": {
            #     pred['variety']: f"{pred['confidence']:.2%}" 
            #     for pred in final_predictions
            # },
            "obtainAt": get_current_datetime_iso()
        }
        
        # Clean up the grain files before sending response
        # processor.cleanup_storage_directory()
        
        result_id = insert_sample_and_identification_result(sample_data,result_data,status)
        
        return jsonify({
            'resultID': str(result_id)
            # 'predictions': final_predictions

        })
        # return jsonify(result_data)

    except Exception as e:
        # Make sure to clean up in case of error
        try:
            processor.cleanup_storage_directory()
        except:
            pass
        return jsonify({'error': str(e)}), 500