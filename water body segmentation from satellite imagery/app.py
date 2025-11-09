import streamlit as st
import cv2
import numpy as np
from tensorflow import keras
from PIL import Image
import io

st.set_page_config(page_title="Water Body Segmentation", page_icon="🌊", layout="wide")

@st.cache_resource
def load_model():
    return keras.models.load_model('water_model_compatible.h5', compile=False)

model = load_model()

st.title("🌊 Water Body Segmentation from Satellite Imagery")
st.write("Upload a satellite image (e.g., from Google Earth) to automatically detect and highlight water bodies.")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Settings")
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05, 
                                     help="Higher values = more conservative detection")
    min_area = st.slider("Minimum Area (pixels)", 100, 2000, 500, 100,
                        help="Filter out small detections")
    overlay_opacity = st.slider("Overlay Opacity", 0.0, 1.0, 0.6, 0.05,
                                help="Transparency of the blue overlay")
    
    st.markdown("---")
    st.markdown("### 📊 Display Options")
    show_mask_only = st.checkbox("Show mask only", value=False)
    show_contours = st.checkbox("Draw contours", value=False)

uploaded_file = st.file_uploader("Choose a satellite image...", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Convert RGBA to RGB if necessary
    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
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
        water_mask = (pred > confidence_threshold).astype(np.uint8) * 255
        water_mask = cv2.resize(water_mask, (w, h), interpolation=cv2.INTER_LINEAR)
        
        # Clean mask
        kernel = np.ones((5, 5), np.uint8)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, kernel)
        
        # Remove small regions
        contours, _ = cv2.findContours(water_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        clean_mask = np.zeros_like(water_mask)
        valid_contours = []
        for contour in contours:
            if cv2.contourArea(contour) > min_area:
                cv2.drawContours(clean_mask, [contour], -1, 255, -1)
                valid_contours.append(contour)
        
        # Smooth
        clean_mask = cv2.GaussianBlur(clean_mask, (5, 5), 0)
        clean_mask = (clean_mask > 127).astype(np.uint8) * 255
        
        # Create visualization
        if show_mask_only:
            output = cv2.cvtColor(clean_mask, cv2.COLOR_GRAY2RGB)
        else:
            # Create blue overlay
            output = original.copy()
            blue_overlay = original.copy()
            blue_overlay[:, :, 2] = 255
            
            mask_3channel = np.stack([clean_mask] * 3, axis=-1) / 255.0
            output = (original * (1 - mask_3channel * overlay_opacity) + 
                     blue_overlay * (mask_3channel * overlay_opacity)).astype(np.uint8)
        
        # Draw contours if requested
        if show_contours and not show_mask_only:
            cv2.drawContours(output, valid_contours, -1, (0, 255, 255), 2)
        
        # Calculate stats
        water_pixels = np.sum(clean_mask > 0)
        total_pixels = clean_mask.shape[0] * clean_mask.shape[1]
        water_percentage = (water_pixels / total_pixels) * 100
        num_water_bodies = len(valid_contours)
    
    with col2:
        st.subheader("💧 Water Segmentation Result")
        st.image(output, use_column_width=True)
    
    # Statistics
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Water Coverage", f"{water_percentage:.2f}%")
    with col_stat2:
        st.metric("Water Bodies Detected", num_water_bodies)
    with col_stat3:
        st.metric("Water Pixels", f"{water_pixels:,}")
    
    # Download button
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        # Save output image
        output_pil = Image.fromarray(output)
        buf = io.BytesIO()
        output_pil.save(buf, format='PNG')
        st.download_button(
            label="📥 Download Segmentation Result",
            data=buf.getvalue(),
            file_name="water_segmentation_result.png",
            mime="image/png"
        )
    
    with col_dl2:
        # Save mask
        mask_pil = Image.fromarray(clean_mask)
        buf_mask = io.BytesIO()
        mask_pil.save(buf_mask, format='PNG')
        st.download_button(
            label="📥 Download Binary Mask",
            data=buf_mask.getvalue(),
            file_name="water_mask.png",
            mime="image/png"
        )
    
else:
    st.info("👆 Please upload a satellite image to get started!")
    
    # Show example info
    st.markdown("### 💡 How to Use")
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        **Supported Water Bodies:**
        - 🏞️ Rivers and streams
        - 🌊 Lakes and reservoirs
        - 🏖️ Coastal areas
        - 🦆 Ponds and wetlands
        """)
    
    with col_info2:
        st.markdown("""
        **Tips for Best Results:**
        - Use high-resolution satellite imagery
        - Ensure good contrast between water and land
        - Adjust confidence threshold for different water types
        - Use minimum area filter to remove noise
        """)
    
    st.markdown("---")
    st.markdown("### 🎯 Example Use Cases")
    st.write("""
    - **Environmental Monitoring**: Track water body changes over time
    - **Urban Planning**: Identify water resources in development areas
    - **Disaster Management**: Assess flood extent and impact
    - **Agriculture**: Monitor irrigation water sources
    - **Conservation**: Map and protect aquatic ecosystems
    """)
