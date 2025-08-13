
import tensorflow as tf
import numpy as np

def load_E(saved_model_path):
    tf.keras.mixed_precision.set_global_policy('mixed_float16')
    
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
    model = tf.keras.models.load_model(
        saved_model_path,
        custom_objects={'loss_fn': loss_fn},
        compile=False  # Set compile=False for inference
    )
    
    # Store the original model before optimization
    # DO NOT apply tf.function to the model itself
    
    # Warm up the model
    dummy_input = tf.random.normal((1, 224, 224, 3))
    model(dummy_input)
    
    # Return the loaded model ready for inference
    return model

def predict_image_E(model, preprocessed_image, class_list):
    """
    Predict the class of an image using the provided model.
    
    Args:
        model: Loaded EfficientNet model
        preprocessed_image: Image preprocessed with EfficientNet preprocessing
        class_list: List of class names
    
    Returns:
        tuple: (predicted_class_name, confidence_score)
    """
    # Make prediction
    print("predicting..... \n\n")
    
    # Use the model directly for prediction
    with tf.device('/GPU:0'):
        # For tf.function optimized prediction
        if hasattr(model, 'predict'):
            predictions = model.predict(preprocessed_image)
        else:
            # Direct call if model is a tf.function
            predictions = model(preprocessed_image).numpy()
    
    print(predictions)
    
    # Get the index of the highest confidence prediction
    predicted_class_index = np.argmax(predictions[0])
    
    # Get the confidence score (probability)
    confidence_score = float(predictions[0][predicted_class_index])
    
    # Get the class name from the class list
    predicted_class_name = class_list[predicted_class_index]
    
    return predicted_class_name, confidence_score

# Optimized predict function that can be used with tf.function
@tf.function(jit_compile=True)
def optimized_predict(model, preprocessed_image):
    """
    GPU-optimized prediction function
    """
    return model(preprocessed_image)