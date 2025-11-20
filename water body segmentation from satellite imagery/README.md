# 🌊 Water Body Segmentation from Satellite Imagery

An AI-powered tool for automatically detecting and segmenting water bodies from satellite imagery using deep learning. Built with TensorFlow and Streamlit for real-time analysis and visualization.

![Water Body Segmentation Demo](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)

## 🎯 Overview

This project provides an interactive web application that uses computer vision and deep learning to identify water bodies in satellite imagery. The model can detect rivers, lakes, coastal areas, ponds, and other water features with adjustable confidence thresholds and filtering options.

**Live Demo**: [Try it on Hugging Face Spaces](https://huggingface.co/spaces/Abiodun360of/water-body-segmentation)

## ✨ Features

- **Real-time Segmentation**: Upload satellite images and get instant water body detection
- **Interactive Controls**: 
  - Adjustable confidence threshold for detection sensitivity
  - Minimum area filtering to remove noise
  - Customizable overlay opacity for better visualization
- **Multiple Visualization Modes**:
  - Overlay mode with transparent blue highlighting
  - Binary mask view for detailed analysis
  - Optional contour drawing for boundary visualization
- **Statistical Analysis**:
  - Water coverage percentage calculation
  - Number of distinct water bodies detected
  - Total water pixel count
- **Export Capabilities**:
  - Download segmentation results as PNG
  - Export binary masks for further analysis

## 🏗️ Architecture

The project uses a deep learning model trained on satellite imagery to perform semantic segmentation:

- **Model**: Custom U-Net architecture (or similar encoder-decoder network)
- **Input**: RGB satellite images (resized to 256×256 for inference)
- **Output**: Pixel-wise binary mask indicating water presence
- **Post-processing**: Morphological operations and contour filtering for clean results

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
pip package manager
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Abiodun360of/Machine-Learning-And-Data-Scinece.git
cd "water body segmentation from satellite imagery"
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure you have the trained model file:
```
water_model_compatible.h5
```

### Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📦 Dependencies

- **streamlit**: Web application framework
- **tensorflow/keras**: Deep learning model inference
- **opencv-python**: Image processing and morphological operations
- **numpy**: Numerical computations
- **Pillow**: Image loading and manipulation

## 🎮 Usage

1. **Upload Image**: Click "Choose a satellite image..." and select a satellite image (JPG, PNG, or JPEG)
2. **Adjust Settings**: Use the sidebar controls to fine-tune detection:
   - **Confidence Threshold**: Higher values = more conservative detection (default: 0.95)
   - **Minimum Area**: Filter out small detections (default: 500 pixels)
   - **Overlay Opacity**: Adjust visualization transparency (default: 0.6)
3. **View Results**: Compare original and segmented images side-by-side
4. **Download**: Save the segmentation result or binary mask for further use

## 🌍 Applications

- **Environmental Monitoring**: Track changes in water bodies over time due to climate change or human activity
- **Urban Planning**: Identify and map water resources for infrastructure development
- **Disaster Management**: Quickly assess flood extent and impact areas
- **Agriculture**: Monitor irrigation water sources and reservoir levels
- **Conservation**: Map aquatic ecosystems for protection and research
- **Hydrology Studies**: Analyze watershed patterns and water distribution

## 📊 Model Performance

The model achieves robust performance on various water body types:
- Rivers and streams
- Lakes and reservoirs
- Coastal areas and shorelines
- Ponds and wetlands

**Tips for Best Results**:
- Use high-resolution satellite imagery
- Ensure good contrast between water and land features
- Adjust confidence threshold based on water type (clear water vs. turbid water)
- Use minimum area filter to eliminate noise from shadows or artifacts

## 🔧 Technical Details

### Image Processing Pipeline

1. **Preprocessing**: Image resizing and normalization
2. **Inference**: Model prediction on processed input
3. **Thresholding**: Binary mask creation based on confidence
4. **Morphological Operations**: Closing and opening to clean mask
5. **Contour Filtering**: Remove small regions below minimum area
6. **Smoothing**: Gaussian blur for natural boundaries
7. **Visualization**: Overlay generation with customizable opacity

### Model Input/Output

- **Input Shape**: (256, 256, 3) - RGB image
- **Output Shape**: (256, 256, 1) - Single channel probability map
- **Preprocessing**: Pixel values normalized to [0, 1]
- **Post-processing**: Resize back to original dimensions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is available for educational and research purposes.

## 👨‍💻 Author

**Abiodun Ogunleye**
- GitHub: [@Abiodun360of](https://github.com/Abiodun360of)
- Hugging Face: [@Abiodun360of](https://huggingface.co/Abiodun360of)

## 🙏 Acknowledgments

- Satellite imagery providers (Google Earth, Sentinel, Landsat)
- Open-source community for deep learning frameworks
- Contributors and users providing feedback

## 📧 Contact

For questions, suggestions, or collaborations, please open an issue on GitHub or reach out through the repository.

---

⭐ **If you find this project useful, please consider giving it a star!**
