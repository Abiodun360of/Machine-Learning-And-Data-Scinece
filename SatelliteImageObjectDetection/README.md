# 🛰️ Satellite Image Object Detection

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Abiodun360of/SatelliteImageObjectDetection)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A deep learning-based object detection system for identifying land features from satellite and aerial imagery using YOLOv8.

![Demo](assets/demo.gif)
*Example of land detection in satellite imagery*

## 🌟 Features

- 🎯 **Accurate Detection**: YOLOv8-based model trained on land detection dataset
- 🖼️ **Easy to Use**: Simple web interface for uploading and analyzing images
- ⚡ **Fast Inference**: Real-time detection with adjustable confidence thresholds
- 🌐 **Web Deployment**: Deployed on Hugging Face Spaces for easy access
- 🔧 **Customizable**: Adjustable parameters (confidence, IOU, image size)

## 🚀 Live Demo

Try the live demo: [Satellite Object Detection on Hugging Face](https://huggingface.co/spaces/Abiodun360of/SatelliteImageObjectDetection)

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Training](#training)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Results](#results)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🔧 Installation

### Prerequisites

- Python 3.10 or higher
- CUDA-compatible GPU (optional, for training)
- 8GB+ RAM recommended

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/satellite-object-detection.git
cd satellite-object-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running Locally

1. **Start the Gradio app**
```bash
python app.py
```

2. **Open browser**
Navigate to `http://localhost:7860`

3. **Upload and detect**
- Upload a satellite/aerial image
- Adjust confidence threshold (default: 0.25)
- Click "Detect Objects"
- View results with bounding boxes

### Using Python API

```python
from ultralytics import YOLO
from PIL import Image

# Load model
model = YOLO('best.pt')

# Run inference
results = model.predict(
    source='path/to/image.jpg',
    conf=0.25,
    imgsz=640
)

# Display results
results[0].show()

# Save results
results[0].save('output.jpg')
```

## 🏋️ Training

### Training Your Own Model

```python
import yaml
from ultralytics import YOLO
import torch

# Configuration
yaml_path = 'data.yaml'
dataset_location = 'path/to/dataset'

# Load dataset config
with open(yaml_path, 'r') as f:
    data_config = yaml.safe_load(f)

# Initialize YOLOv8 model
model = YOLO('yolov8s.pt')

# Check device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Start training
model.train(
    data=yaml_path,
    epochs=100,
    imgsz=640,
    batch=16,
    device=device,
    project='land_detection',
    name='train',
    exist_ok=True,
    pretrained=True
)

print("Training completed! Model saved in: land_detection/train/weights/best.pt")
```

### Training Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Model | YOLOv8s | Small variant for balance of speed/accuracy |
| Epochs | 100 | Training iterations |
| Image Size | 640 | Input image resolution |
| Batch Size | 16 | Adjust based on GPU memory |
| Device | CUDA/CPU | Automatic GPU detection |

## 📊 Dataset

### Dataset Structure

```
dataset/
├── train/
│   ├── images/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── labels/
│       ├── img1.txt
│       ├── img2.txt
│       └── ...
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── data.yaml
```

### data.yaml Format

```yaml
path: /path/to/dataset
train: train/images
val: valid/images
test: test/images

nc: 3  # number of classes
names: ['class1', 'class2', 'class3']  # class names
```

### Label Format (YOLO)

Each `.txt` file contains bounding boxes in YOLO format:
```
class_id x_center y_center width height
```
All values are normalized (0-1).

## 🏗️ Model Architecture

- **Base Model**: YOLOv8s (Small)
- **Input Size**: 640x640 pixels
- **Backbone**: CSPDarknet53
- **Neck**: PANet
- **Head**: YOLO Detection Head
- **Parameters**: ~11.2M

## 📈 Results

### Performance Metrics

| Metric | Value |
|--------|-------|
| mAP@0.5 | 0.373 % |
| mAP@0.5:0.95 | 0.255% |
| R | 0.475 % |

## 🌐 Deployment

### Hugging Face Spaces

The model is deployed on Hugging Face Spaces:
- **URL**: https://huggingface.co/spaces/Abiodun360of/SatelliteImageObjectDetection
- **Framework**: Gradio
- **Hardware**: CPU Basic (upgradable to GPU)

### Deploy Your Own

1. Create a Hugging Face account
2. Create new Space (select Gradio SDK)
3. Upload files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `best.pt` (your model)
4. Space will automatically build and deploy



## 📝 Project Structure

```
satellite-object-detection/
├── app.py                  # Gradio web interface
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── best.pt                # Trained model weights
├── train.py               # Training script
├── data.yaml              # Dataset configuration
├── assets/                # Images and media
│   └── demo.gif
├── examples/              # Example images
│   ├── example1.jpg
│   └── example2.jpg
├── results/               # Detection results
├── notebooks/             # Jupyter notebooks
│   └── training.ipynb
└── utils/                 # Utility functions
    ├── __init__.py
    └── helpers.py
```

## 🔍 Troubleshooting

### Common Issues

**Issue**: Model not loading
```bash
# Ensure model file exists
ls -lh best.pt

# Check file integrity
python -c "from ultralytics import YOLO; model = YOLO('best.pt'); print('Model loaded!')"
```

**Issue**: CUDA out of memory
```python
# Reduce batch size in training
model.train(batch=8)  # or smaller

# Use smaller image size
model.train(imgsz=416)
```

**Issue**: Low accuracy
- Increase training epochs
- Use data augmentation
- Collect more training data
- Try larger model (yolov8m or yolov8l)

## 📚 Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)
- [Google Earth Engine](https://earthengine.google.com/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/YOUR_USERNAME)

## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- Hugging Face for hosting
- Google Earth Pro for satellite imagery
- Contributors and testers

## 📞 Contact

- **Email**: abiodun360of@gmail.com
- **Hugging Face**: [@Abiodun360of](https://huggingface.co/Abiodun360of)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/satellite-object-detection&type=Date)](https://star-history.com/#YOUR_USERNAME/satellite-object-detection&Date)

---

**Made with ❤️ using YOLOv8 and Gradio**

If you find this project useful, please consider giving it a ⭐!
