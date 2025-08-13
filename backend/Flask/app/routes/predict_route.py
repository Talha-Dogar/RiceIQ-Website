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
from ..models.ml_models.utils.preprocess_MobileNet import load_and_preprocess_image
from ..models.ml_models.efficient import load_E
from ..models.ml_models.utils.preprocess_EfficientNet import load_and_preprocess_image_E
from ..models.ml_models.efficient import predict_image_E
from ..models.ml_models.utils.conf_gpu import configure_gpu
predict_bp = Blueprint('predict', __name__)
def get_current_datetime_iso():
    return datetime.now().replace(microsecond=0).isoformat()


configure_gpu()

mobilenet_path = "/mnt/e/imp/Web/backend/Flask/app/models/ml_models/saved_files/efficientnet.keras"
mobilenet_model = load_E(mobilenet_path)
print(mobilenet_model,"\n\n")
@predict_bp.route('/predict', methods=['POST'])
def predict():
    print("predict api")
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        riceVarieties = {
    0: '1509',
    1: 'Basmati-2000',
    2: 'IR-6',
    3: 'PK-1121',
    4: 'PK-386',
    5: 'Sela',
    6: 'SuperBasmati',
    7: 'Supri'
}

        # Save the image file
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        # preprocess image
        processed_img = load_and_preprocess_image_E(file_path)
        if processed_img is not None:
            print("preprocessed \n\n")
        # Mocked model prediction
          
        # Use with GPU
        with tf.device('/GPU:0'):
            rice_variety, confidence = predict_image_E(mobilenet_model, processed_img, riceVarieties)
        # rice_variety,confidence =predict_image(mobilenet_model,processed_img,riceVarieties)
        

        # Prepare data for MongoDB
        sample_data = {
            "imgUrl": file_path,
            "createdAt": get_current_datetime_iso()
        }

        result_data = {
            "confidenceScore": f"{confidence:.2%}",
            "varietyNames": [rice_variety],
            "adulterationStatus": "False",
            "percentageComposition": {rice_variety: 100},
            "obtainAt": get_current_datetime_iso()  
        }

        # Insert into DB
        result_id = insert_sample_and_result(sample_data, result_data)

        response = {
            
            'resultID': str(result_id),
        }
        return jsonify(response)

    except Exception as e:
        print( jsonify({'error': str(e)}))
        return jsonify({'error': str(e)}), 500
