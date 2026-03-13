
GPU-Accelerated Land Cover Classification using CUDA and K-Means
Overview

This project demonstrates GPU acceleration for satellite image analysis using CUDA-based libraries. The goal is to compare CPU vs GPU performance for vegetation feature extraction and land cover classification.

The workflow simulates satellite imagery similar to data from
Landsat 9
The experiment shows how GPU computing significantly speeds up remote sensing pipelines used in geospatial analytics and machine learning.

Research Objective

Satellite imagery processing can be computationally expensive because images contain millions of pixels and multiple spectral bands.

This project investigates:

How GPU computing accelerates NDVI computation

How GPU K-Means clustering improves land cover classification performance

The performance difference between CPU and GPU implementations

Vegetation Index (NDVI)

Vegetation health is computed using the Normalized Difference Vegetation Index (NDVI).

NDVI = \frac{NIR - Red}{NIR + Red}

Where:

NIR = Near Infrared band

Red = Red spectral band

Higher NDVI values indicate healthy vegetation.

Project Pipeline
Satellite Bands (Red + NIR)
        │
        ▼
NDVI Computation
(CPU vs GPU)
        │
        ▼
Feature Matrix
(Red, NIR, NDVI)
        │
        ▼
K-Means Clustering
(CPU vs GPU)
        │
        ▼
Land Cover Classification Map
Technologies Used
Technology	Purpose
Python	Main programming language
NumPy	CPU numerical computing
CuPy	GPU-accelerated NumPy operations
scikit-learn	CPU K-Means clustering
cuML (RAPIDS)	GPU K-Means clustering
Google Colab	Cloud GPU environment
Matplotlib	Visualization

The project runs on GPU hardware such as
NVIDIA Tesla T4.

Experimental Setup

Satellite bands are simulated to represent large satellite imagery.

Image size used:

4096 × 4096 pixels

Features used for classification:

Red band

Near Infrared band

NDVI vegetation index

Clustering algorithm:

K-Means (k = 3 clusters)

Clusters represent approximate land cover classes such as:

vegetation

water

urban areas

Performance Results

Example benchmark results:

Task	CPU Time	GPU Time	Speedup
NDVI Computation	0.33s	0.03 s	10×
K-Means Clustering	370.9 s	9.9 s	37×

These results demonstrate the benefit of GPU acceleration for large-scale satellite data analysis.

Visualization

The project generates two outputs:

NDVI Vegetation Map

Shows vegetation health across the image.

Land Cover Classification

K-Means clusters representing different land cover types.

Repository Structure
gpu-landcover-cuda
│
├── notebook.ipynb
│
├── data/
│   ├── red_band.npy
│   └── nir_band.npy
│
├── results/
│   ├── ndvi_map.png
│   └── landcover_map.png
│
└── README.md
How to Run

Open the notebook in Google Colab and enable GPU.

Runtime → Change Runtime Type → GPU

Install dependencies:

pip install cupy-cuda12x
pip install cuml-cu12x
pip install scikit-learn

Run the notebook cells sequentially to reproduce the experiment.

Applications

GPU-accelerated remote sensing has applications in:

vegetation monitoring

land cover mapping

environmental monitoring

precision agriculture

climate change analysis

Future Improvements

Possible extensions include:

Using real satellite imagery from Sentinel-2

Implementing GPU-based convolution filters

Training deep learning models such as ResNet for land cover classification

Building a real-time geospatial analysis pipeline

Author

Ofobutu Abiodun Emmanuel

Data Analyst | Spatial Data Analyst (GIS) | Machine Learning Enthusiast

Skills:

Remote Sensing & GIS

Machine Learning

CUDA GPU Computing

Python & Data Science
