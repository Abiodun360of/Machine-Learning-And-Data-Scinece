import streamlit as st
import cv2
import numpy as np
from tensorflow import keras
from PIL import Image

st.set_page_config(page_title="Water Body Segmentation", page_icon="🌊", layout="wide")

@st.cache_resource
def load_model():
    return keras.models.load_model('water_model_compatible.h5', compile=False)

model = load_model()

st.title("🌊 Water Body Segmentation from Satellite Imagery")
st.write("Upload a satellite image (e.g., from Google Earth) to automatically detect and highlight water bodies.")

uploaded_file = st.file_uploader("Choose a satellite image...", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Convert RGBA to RGB if necessary
    if image.mode == 'RGBA':
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    original = np.array(image)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Original Image")
        st.image(original, use_column_width=True)
    
    with st.spinner('🔍 Analyzing water bodies...'):
        h, w = original.shape[:2]
        
        # Predict
        img_resized = cv2.resize(original, (256, 256))
        img_input = np.expand_dims(img_resized.astype(np.float32) / 255.0, 0)
        pred = model.predict(img_input, verbose=0)[0].squeeze()
        water_mask = (pred > 0.5).astype(np.uint8) * 255
        water_mask = cv2.resize(water_mask, (w, h), interpolation=cv2.INTER_LINEAR)
        
        # Clean mask
        kernel = np.ones((5, 5), np.uint8)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, kernel)
        
        # Remove small regions
        contours, _ = cv2.findContours(water_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        clean_mask = np.zeros_like(water_mask)
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                cv2.drawContours(clean_mask, [contour], -1, 255, -1)
        
        # Smooth
        clean_mask = cv2.GaussianBlur(clean_mask, (5, 5), 0)
        clean_mask = (clean_mask > 127).astype(np.uint8) * 255
        
        # Create blue overlay
        output = original.copy()
        blue_overlay = original.copy()
        blue_overlay[:, :, 2] = 255
        
        mask_3channel = np.stack([clean_mask] * 3, axis=-1) / 255.0
        output = (original * (1 - mask_3channel * 0.6) + blue_overlay * (mask_3channel * 0.6)).astype(np.uint8)
        
        # Calculate stats
        water_pixels = np.sum(clean_mask > 0)
        total_pixels = clean_mask.shape[0] * clean_mask.shape[1]
        water_percentage = (water_pixels / total_pixels) * 100
    
    with col2:
        st.subheader("💧 Water Segmentation Result")
        st.image(output, use_column_width=True)
    
    st.success(f"✅ Water coverage: **{water_percentage:.2f}%** of image")
    
else:
    st.info("👆 Please upload a satellite image to get started!")
    
    # Show example
    st.markdown("### Example")
    st.write("This AI model can detect rivers, lakes, ponds, and coastal water bodies from satellite imagery.")