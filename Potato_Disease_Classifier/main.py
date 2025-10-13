import gradio as gr
import numpy as np
from PIL import Image
import tensorflow as tf
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "potatoes.h5")

# Load model once
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

# Prediction function
def predict_image(image: Image.Image):
    image = image.resize((256, 256))        # Resize if needed
    img_array = np.array(image) / 255.0
    img_batch = np.expand_dims(img_array, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))
    return {predicted_class: confidence}

# Gradio interface
demo = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(type="pil", label="Upload Potato Leaf"),
    outputs=gr.Label(num_top_classes=3),
    title="Potato Disease Classifier",
    description="Upload a potato leaf image to detect Early Blight, Late Blight, or Healthy leaf."
)

if __name__ == "__main__":
    demo.launch()
