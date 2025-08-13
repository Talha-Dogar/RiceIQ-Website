import tensorflow as tf
import numpy as np
def load(saved_model_path):
    # Define custom categorical focal loss
    def categorical_focal_loss(gamma=2.0, alpha=0.25):
        """
        Focal loss for multi-class classification.
        Computes the loss per sample by scaling the standard cross-entropy loss.
        """
        def loss_fn(y_true, y_pred):
            epsilon = tf.keras.backend.epsilon()  # avoid log(0)
            y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
            cross_entropy = -y_true * tf.math.log(y_pred)
            focal_factor = alpha * tf.math.pow(1 - y_pred, gamma)
            loss = focal_factor * cross_entropy
            return tf.reduce_sum(loss, axis=1)
        return loss_fn
    
    # Load the fine-tuned model with the custom loss for inference
    loss_fn = categorical_focal_loss(gamma=2.0, alpha=0.25)
    
    # Load model with compile=False for inference only
    inference_model = tf.keras.models.load_model(
        saved_model_path,
        custom_objects={'loss_fn': loss_fn},
        compile=False  # Set compile=False for inference
    )
    
    # Return the loaded model ready for inference
    return inference_model

def predict_image(model, preprocessed_image, class_list):
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
    print("predicting..... \n\n")
    predictions = model.predict(preprocessed_image)
    print(predictions)
    # Get the index of the highest confidence prediction
    predicted_class_index = np.argmax(predictions[0])
    
    # Get the confidence score (probability)
    confidence_score = float(predictions[0][predicted_class_index])
    
    # Get the class name from the class list
    predicted_class_name = class_list[predicted_class_index]
    
    return predicted_class_name, confidence_score