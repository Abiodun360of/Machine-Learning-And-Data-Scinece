# 🥔 Potato Disease Classifier


An intelligent deep learning system that identifies and diagnoses potato plant diseases from leaf images using Convolutional Neural Networks (CNN). This agricultural AI solution helps farmers detect Early Blight, Late Blight, and assess healthy plants, enabling timely intervention to protect crops and improve yield outcomes.

![Potato Disease Classification](https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=1200&h=400&fit=crop)

## 🌟 Features

- **Real-time Disease Detection**: Upload a potato leaf image and get instant classification
- **Multi-class Classification**: Identifies three categories:
  - Early Blight (Alternaria solani)
  - Late Blight (Phytophthora infestans)
  - Healthy leaves
- **Smart Validation**: Automatically rejects non-leaf images (people, objects, etc.)
- **High Accuracy**: Trained on extensive potato leaf dataset with data augmentation
- **User-friendly Interface**: Built with Gradio for easy web deployment

## 🚀 Live Demo

Try the live application: https://huggingface.co/spaces/Abiodun360of/potato_disease_classifier/

## 📊 Model Architecture

The model uses a deep Convolutional Neural Network with the following architecture:

```
Input (256x256x3)
    ↓
Data Augmentation (Random Flip, Rotation)
    ↓
6x Conv2D (32, 64, 64, 64, 64, 64 filters) + MaxPooling2D
    ↓
Flatten
    ↓
Dense (64 units, ReLU)
    ↓
Dense (3 units, Softmax)
```

### Training Details

- **Image Size**: 256x256 pixels
- **Batch Size**: 32
- **Epochs**: 50
- **Optimizer**: Adam (learning rate: 0.001)
- **Loss Function**: Sparse Categorical Crossentropy
- **Data Split**: 70% Training, 15% Validation, 15% Testing
- **Data Augmentation**: Random horizontal/vertical flips and rotations

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- TensorFlow 2.x
- Gradio
- PIL (Pillow)
- NumPy

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Abiodun360of/Machine-Learning-And-Data-Scinece.git
cd Machine-Learning-And-Data-Scinece/Potato_Disease_Classifier
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download the trained model**
   - The trained model `potatoes.h5` should be in the project directory

4. **Run the application**
```bash
python app.py
```

The app will launch at `http://localhost:7860`

## 📝 Usage

### Training the Model

```python
import tensorflow as tf
from tensorflow.keras import models, layers

# Load dataset
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "path/to/Potato_Leaf_Disease_Dataset",
    shuffle=True,
    image_size=(256, 256),
    batch_size=32
)

# Build model
model = models.Sequential([
    layers.Resizing(256, 256),
    layers.Rescaling(1./255),
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    # ... additional layers
    layers.Dense(3, activation='softmax')
])

# Compile and train
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(train_ds, epochs=50, validation_data=val_ds)
model.save("potatoes.h5")
```

### Making Predictions

```python
from PIL import Image
import numpy as np

# Load image
img = Image.open("potato_leaf.jpg")

# Preprocess
img_resized = img.resize((256, 256))
img_array = np.array(img_resized).astype('float32') / 255.0
img_batch = np.expand_dims(img_array, 0)

# Predict
predictions = model.predict(img_batch)
class_names = ["Early Blight", "Late Blight", "Healthy"]
result = class_names[np.argmax(predictions[0])]
confidence = np.max(predictions[0])

print(f"Prediction: {result} ({confidence*100:.2f}%)")
```

## 🧪 Validation System

The application includes a multi-layered validation system to ensure only potato leaf images are classified:

1. **Color Analysis**: Checks for green tones typical in leaves
2. **Brightness Check**: Filters out overly dark/bright images
3. **Texture Analysis**: Ensures sufficient color variation
4. **Skin Tone Detection**: Rejects images of people

Images that fail validation return an error message instead of a classification.

## 📁 Project Structure

```
Potato_Disease_Classifier/
├── app.py                  # Gradio web application
├── training_notebook.ipynb # Model training code
├── potatoes.h5            # Trained model weights
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🎯 Performance

The model achieves high accuracy on the test set:
- Training accuracy: ~95%+
- Validation accuracy: ~93%+
- Robust to various lighting conditions and leaf orientations

## 🔬 Dataset

The model was trained on a comprehensive dataset of potato leaf images containing:
- Early Blight samples
- Late Blight samples
- Healthy leaf samples

Images were augmented during training to improve model robustness.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Abiodun**
- GitHub: [@Abiodun360of](https://github.com/Abiodun360of)
- Hugging Face: [@Abiodun360of](https://huggingface.co/Abiodun360of)
- Linkedln : https://www.linkedin.com/in/abiodun360of

## 🙏 Acknowledgments

- Dataset providers and agricultural research community
- TensorFlow and Gradio teams
- Open source community

## 📞 Contact

For questions, suggestions, or collaborations, feel free to reach out through GitHub issues or pull requests.

---

**Note**: This tool is designed to assist farmers and agricultural professionals but should not replace expert agricultural advice for critical decisions.
