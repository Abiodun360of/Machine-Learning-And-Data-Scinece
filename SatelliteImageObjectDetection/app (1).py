import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import torch
from torchvision import transforms, models

def create_placeholder_image():
    """Create a placeholder image for when no model is loaded"""
    img = Image.new('RGB', (800, 600), color='#4A90E2')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    title = "🛰️ Satellite Object Detection"
    draw.text((150, 200), title, fill='white', font=title_font)
    
    subtitle = "Upload satellite or aerial images"
    draw.text((200, 300), subtitle, fill='white', font=subtitle_font)
    
    draw.ellipse([350, 380, 450, 480], fill='white', outline='white')
    draw.rectangle([390, 350, 410, 390], fill='white')
    draw.polygon([(370, 430), (330, 450), (370, 470)], fill='white')
    draw.polygon([(430, 430), (470, 450), (430, 470)], fill='white')
    
    return img

# Load image classifier (ResNet50 pre-trained on ImageNet)
print("Loading image classifier...")
try:
    classifier = models.resnet50(pretrained=True)
    classifier.eval()
    CLASSIFIER_LOADED = True
    print("✅ Image classifier loaded successfully!")
except Exception as e:
    CLASSIFIER_LOADED = False
    print(f"❌ Error loading classifier: {e}")

# Image preprocessing for classifier
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ImageNet classes that indicate satellite/aerial imagery
SATELLITE_KEYWORDS = [
    'valley', 'volcano', 'promontory', 'seashore', 'lakeside', 'sandbar',
    'cliff', 'coral reef', 'geyser', 'alp', 'mountain', 'canyon',
    'dam', 'breakwater', 'dock', 'crane', 'pier', 'beacon', 'lighthouse',
    'airship', 'warplane', 'missile', 'aircraft carrier', 'submarine',
    'container ship', 'drilling platform', 'space shuttle', 'solar dish',
    'wing', 'runway', 'barn', 'greenhouse', 'palace', 'monastery',
    'castle', 'church', 'planetarium', 'stadium', 'megalith'
]

# Load ImageNet class labels
IMAGENET_CLASSES_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"

try:
    import urllib.request
    import json
    with urllib.request.urlopen(IMAGENET_CLASSES_URL) as url:
        imagenet_classes = json.loads(url.read().decode())
    print("✅ ImageNet classes loaded")
except:
    imagenet_classes = None
    print("⚠️ Could not load ImageNet classes")

# Try to load YOLO detection model
try:
    from ultralytics import YOLO
    
    custom_model_path = 'best.pt'
    if os.path.exists(custom_model_path):
        detection_model = YOLO(custom_model_path)
        DETECTION_MODEL_LOADED = True
        MODEL_TYPE = "custom"
        class_names = detection_model.names
        print(f"✅ Custom detection model loaded! Classes: {class_names}")
    else:
        print(f"⚠️ Custom model '{custom_model_path}' not found. Using pre-trained YOLOv8n...")
        detection_model = YOLO('yolov8n.pt')
        DETECTION_MODEL_LOADED = True
        MODEL_TYPE = "pretrained"
        class_names = detection_model.names
        print(f"✅ Pre-trained YOLOv8n loaded! Classes: {len(class_names)} COCO classes")
        
except Exception as e:
    DETECTION_MODEL_LOADED = False
    MODEL_TYPE = None
    class_names = {}
    print(f"❌ Error loading detection model: {e}")

def is_satellite_image(image, top_k=5):
    """
    Classify if image is satellite/aerial imagery using pre-trained ResNet50
    Returns: (is_satellite, confidence, predictions)
    """
    if not CLASSIFIER_LOADED or imagenet_classes is None:
        return True, 1.0, ["Classification unavailable - proceeding with detection"]
    
    try:
        # Preprocess image
        img_tensor = preprocess(image)
        img_tensor = img_tensor.unsqueeze(0)
        
        # Get predictions
        with torch.no_grad():
            outputs = classifier(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
        # Get top predictions
        top_prob, top_indices = torch.topk(probabilities, top_k)
        
        predictions = []
        satellite_score = 0
        
        for prob, idx in zip(top_prob, top_indices):
            class_name = imagenet_classes[idx.item()]
            predictions.append(f"{class_name}: {prob.item():.1%}")
            
            # Check if prediction indicates satellite/aerial imagery
            if any(keyword in class_name.lower() for keyword in SATELLITE_KEYWORDS):
                satellite_score += prob.item()
        
        # Consider it satellite imagery if score is above threshold or top prediction matches
        is_satellite = satellite_score > 0.15 or any(
            keyword in imagenet_classes[top_indices[0].item()].lower() 
            for keyword in SATELLITE_KEYWORDS
        )
        
        return is_satellite, satellite_score, predictions
        
    except Exception as e:
        print(f"Classification error: {e}")
        return True, 1.0, ["Classification error - proceeding with detection"]

def predict(image, confidence_threshold, iou_threshold, image_size, skip_classification):
    """Run prediction on the uploaded image with satellite image validation"""
    
    if not DETECTION_MODEL_LOADED:
        error_msg = """
        ❌ Detection model not loaded!
        
        Please ensure YOLO model is available.
        """
        return image, error_msg
    
    if image is None:
        return create_placeholder_image(), "⚠️ Please upload an image first!"
    
    try:
        result_text = ""
        
        # Step 1: Classify if it's satellite imagery (unless skipped)
        if not skip_classification:
            result_text += "🔍 **Step 1: Image Classification**\n\n"
            is_satellite, sat_confidence, predictions = is_satellite_image(image)
            
            result_text += f"Satellite imagery score: {sat_confidence:.1%}\n\n"
            
            if not is_satellite:
                result_text += "❌ **This does not appear to be satellite or aerial imagery!**\n\n"
                result_text += "⚠️ The model is trained specifically for satellite/aerial images.\n"
                result_text += "Please upload:\n"
                result_text += "  • Satellite imagery\n"
                result_text += "  • Aerial photographs\n"
                result_text += "  • Drone footage\n"
                result_text += "  • Maps or geographic views\n\n"
                result_text += "Or check 'Skip Classification' to force detection anyway."
                
                # Return original image with warning overlay
                img_with_warning = image.copy()
                draw = ImageDraw.Draw(img_with_warning)
                
                # Add semi-transparent red overlay
                overlay = Image.new('RGBA', img_with_warning.size, (255, 0, 0, 100))
                img_with_warning = Image.alpha_composite(
                    img_with_warning.convert('RGBA'), 
                    overlay
                ).convert('RGB')
                
                return img_with_warning, result_text
            
            result_text += "✅ **Satellite/Aerial imagery detected!**\n"
            result_text += "Proceeding with object detection...\n\n"
        
        # Step 2: Object Detection
        result_text += "🎯 **Step 2: Object Detection**\n"
        result_text += f"Model: {'Custom satellite model' if MODEL_TYPE == 'custom' else 'Pre-trained YOLOv8n'}\n\n"
        
        # Run inference
        results = detection_model.predict(
            source=image,
            conf=confidence_threshold,
            iou=iou_threshold,
            imgsz=int(image_size),
            verbose=False
        )
        
        result = results[0]
        plotted_img = result.plot()
        plotted_img_rgb = cv2.cvtColor(plotted_img, cv2.COLOR_BGR2RGB)
        
        # Format detection results
        detections = []
        if len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].tolist()
                
                detections.append({
                    'class': class_names.get(class_id, f'Class {class_id}'),
                    'confidence': confidence,
                    'bbox': bbox
                })
        
        if len(detections) == 0:
            result_text += "🔍 No objects detected.\n\nTry:\n"
            result_text += "  • Lowering the confidence threshold\n"
            result_text += "  • Using a different image\n"
            result_text += "  • Checking image quality\n"
        else:
            result_text += f"✅ **Found {len(detections)} object(s)**\n\n"
            
            # Count by class
            class_counts = {}
            for det in detections:
                class_name = det['class']
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            result_text += "📊 **Summary:**\n"
            for class_name, count in class_counts.items():
                result_text += f"  • {class_name}: {count}\n"
            
            result_text += "\n📝 **Details:**\n"
            for i, det in enumerate(detections, 1):
                result_text += f"\n{i}. **{det['class']}**\n"
                result_text += f"   Confidence: {det['confidence']:.1%}\n"
                result_text += f"   Location: [{det['bbox'][0]:.0f}, {det['bbox'][1]:.0f}, {det['bbox'][2]:.0f}, {det['bbox'][3]:.0f}]\n"
        
        return Image.fromarray(plotted_img_rgb), result_text
        
    except Exception as e:
        error_text = f"❌ **Error during prediction:**\n{str(e)}\n\n"
        error_text += "Please try:\n  • A different image\n  • Lower image size\n  • Different settings"
        return image, error_text

# Create the Gradio interface
with gr.Blocks(title="Satellite Object Detection", theme=gr.themes.Soft()) as demo:
    
    # Header
    if DETECTION_MODEL_LOADED:
        if MODEL_TYPE == "custom":
            status_color = "green"
            status_icon = "✅"
            status_msg = "Custom satellite model loaded"
        else:
            status_color = "orange"
            status_icon = "⚠️"
            status_msg = "Using pre-trained YOLOv8n (general purpose)"
    else:
        status_color = "red"
        status_icon = "❌"
        status_msg = "Detection model failed to load"
    
    classifier_status = "✅ Image classifier active" if CLASSIFIER_LOADED else "⚠️ Classifier unavailable"
    
    gr.HTML(f"""
        <div style="text-align: center; max-width: 900px; margin: 0 auto;">
            <h1>🛰️ Smart Satellite Object Detection</h1>
            <p style="color: {status_color}; font-weight: bold;">{status_icon} {status_msg}</p>
            <p style="color: {'green' if CLASSIFIER_LOADED else 'orange'};">{classifier_status}</p>
            <p>Two-stage detection: First validates satellite imagery, then detects objects</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(
                type="pil",
                label="📤 Upload Image"
            )
            
            confidence_slider = gr.Slider(
                minimum=0.1,
                maximum=0.95,
                value=0.25,
                step=0.05,
                label="Confidence Threshold",
                info="Lower = more detections"
            )
            
            skip_classification = gr.Checkbox(
                label="Skip satellite image classification",
                value=False,
                info="Force detection even on non-satellite images"
            )
            
            with gr.Accordion("⚙️ Advanced Settings", open=False):
                iou_slider = gr.Slider(
                    minimum=0.1,
                    maximum=0.95,
                    value=0.45,
                    step=0.05,
                    label="IOU Threshold",
                    info="Non-maximum suppression"
                )
                
                image_size = gr.Slider(
                    minimum=320,
                    maximum=1280,
                    value=640,
                    step=64,
                    label="Image Size",
                    info="Larger = more detail but slower"
                )
            
            predict_btn = gr.Button("🔍 Analyze Image", variant="primary", size="lg")
            
            if DETECTION_MODEL_LOADED and class_names:
                with gr.Accordion("📋 Detectable Classes", open=False):
                    classes_text = ", ".join([f"{v}" for k, v in sorted(class_names.items())])
                    gr.Markdown(f"**{len(class_names)} classes:** {classes_text}")
        
        with gr.Column():
            output_image = gr.Image(
                type="pil",
                label="🎯 Detection Results"
            )
            
            output_text = gr.Textbox(
                label="📊 Analysis Report",
                lines=20,
                max_lines=25
            )
    
    gr.HTML("""
        <div style="text-align: center; margin-top: 20px; padding: 20px; background: #f0f7ff; border-radius: 10px;">
            <h3>🔄 How it works:</h3>
            <div style="text-align: left; max-width: 700px; margin: 0 auto;">
                <p><strong>Step 1:</strong> Pre-trained ResNet50 classifier checks if image is satellite/aerial imagery</p>
                <p><strong>Step 2:</strong> If validated, YOLO model detects objects in the image</p>
                <p><strong>Result:</strong> Prevents misclassification of regular photos as satellite features</p>
            </div>
        </div>
    """)
    
    predict_btn.click(
        fn=predict,
        inputs=[input_image, confidence_slider, iou_slider, image_size, skip_classification],
        outputs=[output_image, output_text]
    )

if __name__ == "__main__":
    demo.launch(show_error=True)