---
title: Laptop Price Predictor
emoji: 💻
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# 💻 Laptop Price Predictor

Machine learning model that predicts laptop prices based on specifications.

## 🌟 Features

- **Accurate Price Predictions**: Get estimated prices in USD based on laptop specs
- **Multiple Brands**: Supports various laptop manufacturers
- **Detailed Specifications**: Input RAM, storage, CPU, GPU, and more
- **Real-time Results**: Instant predictions with detailed breakdowns
- **User-friendly Interface**: Clean and intuitive Gradio interface

## 🔧 How It Works

The model analyzes:
- Brand and laptop type
- Hardware specifications (RAM, Storage)
- Processor and graphics card
- Display features (Touchscreen, IPS)
- Operating system

It then predicts the market price based on historical data and machine learning algorithms.

## 🚀 Usage

1. Select the laptop brand and type
2. Configure hardware specifications
3. Choose display and graphics options
4. Select operating system
5. Click "Predict Price" to get the estimate

## 📊 Model Information

- **Currency**: Predictions in USD (converted from INR)
- **Exchange Rate**: 1 INR = $0.01171 USD
- **Categories**: Multiple laptop brands, types, and configurations

## 🛠️ Tech Stack

- Python
- Scikit-learn
- Gradio
- Pandas
- NumPy

## 📝 Note

Prices are estimates based on historical data and may not reflect current market conditions.
