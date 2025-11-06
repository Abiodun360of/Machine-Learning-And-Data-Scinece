import gradio as gr
import util

# Load artifacts when app starts
util.load_saved_artifacts()

# Current exchange rate (INR to USD)
INR_TO_USD_RATE = 0.01171  # 1 INR = 0.01171 USD

def convert_inr_to_usd(inr_amount):
    """Convert Indian Rupees to US Dollars"""
    return round(inr_amount * INR_TO_USD_RATE, 2)

def predict_price(company, type_name, ram, touchscreen, ips, total_storage, 
                  cpu_brand, gpu_brand, os_type):
    """
    Predict laptop price based on specifications
    """
    try:
        # Validate inputs
        validation = util.validate_inputs(
            company, type_name, cpu_brand, gpu_brand, os_type
        )
        
        if not validation['valid']:
            error_msg = "❌ **Invalid inputs:**\n\n"
            for error in validation['errors']:
                error_msg += f"  • {error}\n"
            return error_msg
        
        # Make prediction (returns price in INR)
        estimated_price_inr = util.get_estimated_price(
            company=company,
            ram=int(ram),
            touchscreen=int(touchscreen),
            ips=int(ips),
            total_storage=int(total_storage),
            type_name=type_name,
            cpu_brand=cpu_brand,
            gpu_brand=gpu_brand,
            os_type=os_type
        )
        
        if estimated_price_inr is None:
            return "❌ **Prediction failed.** Please check your inputs and try again."
        
        # Convert INR to USD
        estimated_price_usd = convert_inr_to_usd(estimated_price_inr)
        
        # Format result
        result = f"""
### 💰 Estimated Price

**${estimated_price_usd:,.2f} USD**

*(₹{estimated_price_inr:,.2f} INR)*

---

#### 📊 Specifications Summary:
- **Brand:** {company}
- **Type:** {type_name}
- **RAM:** {ram} GB
- **Storage:** {total_storage} GB
- **CPU:** {cpu_brand}
- **GPU:** {gpu_brand}
- **OS:** {os_type}
- **Touchscreen:** {'Yes' if touchscreen == 1 else 'No'}
- **IPS Display:** {'Yes' if ips == 1 else 'No'}

---

*Exchange Rate: 1 INR = ${INR_TO_USD_RATE} USD*
"""
        
        return result
        
    except Exception as e:
        return f"❌ **Error:** {str(e)}\n\nPlease check your inputs and try again."

# Get options from util
companies = util.get_company_names()
type_names = util.get_type_names()
cpu_brands = util.get_cpu_brands()
gpu_brands = util.get_gpu_brands()
os_types = util.get_os_types()

# Create Gradio interface
with gr.Blocks(title="Laptop Price Predictor", theme=gr.themes.Soft()) as demo:
    
    gr.HTML("""
        <div style="text-align: center; max-width: 900px; margin: 0 auto;">
            <h1>💻 Laptop Price Predictor</h1>
            <p style="font-size: 18px;">Get accurate price estimates based on laptop specifications</p>
            <p style="color: #666;">Powered by Machine Learning</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🏷️ Basic Information")
            
            company = gr.Dropdown(
                choices=companies,
                label="Brand / Manufacturer",
                value=companies[0] if companies else None,
                info="Select the laptop brand"
            )
            
            type_name = gr.Dropdown(
                choices=type_names,
                label="Laptop Type",
                value=type_names[0] if type_names else None,
                info="Gaming, Ultrabook, Notebook, etc."
            )
            
            gr.Markdown("### 🔧 Hardware Specifications")
            
            ram = gr.Slider(
                minimum=2,
                maximum=64,
                value=8,
                step=2,
                label="RAM (GB)",
                info="Memory capacity"
            )
            
            total_storage = gr.Slider(
                minimum=128,
                maximum=2000,
                value=512,
                step=128,
                label="Total Storage (GB)",
                info="HDD + SSD combined storage"
            )
            
            cpu_brand = gr.Dropdown(
                choices=cpu_brands,
                label="CPU / Processor",
                value=cpu_brands[0] if cpu_brands else None,
                info="Processor brand and model"
            )
            
        with gr.Column():
            gr.Markdown("### 🖥️ Display & Graphics")
            
            touchscreen = gr.Radio(
                choices=[(0, "No"), (1, "Yes")],
                label="Touchscreen",
                value=0,
                info="Does it have touchscreen capability?"
            )
            
            ips = gr.Radio(
                choices=[(0, "No"), (1, "Yes")],
                label="IPS Display",
                value=1,
                info="In-Plane Switching display technology"
            )
            
            gpu_brand = gr.Dropdown(
                choices=gpu_brands,
                label="GPU / Graphics Card",
                value=gpu_brands[0] if gpu_brands else None,
                info="Graphics processing unit"
            )
            
            gr.Markdown("### 💿 Software")
            
            os_type = gr.Dropdown(
                choices=os_types,
                label="Operating System",
                value=os_types[0] if os_types else None,
                info="Pre-installed OS"
            )
            
            predict_btn = gr.Button(
                "🔍 Predict Price", 
                variant="primary", 
                size="lg",
                scale=2
            )
    
    output = gr.Markdown(
        label="Prediction Result",
        value="*Enter specifications and click 'Predict Price' to get an estimate*"
    )
    
    predict_btn.click(
        fn=predict_price,
        inputs=[company, type_name, ram, touchscreen, ips, total_storage, 
                cpu_brand, gpu_brand, os_type],
        outputs=output
    )
    
    gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white;">
            <h3 style="margin-top: 0;">💡 How It Works</h3>
            <p style="max-width: 700px; margin: 10px auto;">
                This machine learning model analyzes laptop specifications and predicts 
                market prices based on historical data. Adjust the specifications above 
                to see how different features affect the price.
            </p>
        </div>
    """)

if __name__ == "__main__":
    print("🚀 Starting Laptop Price Prediction App...")
    print(f"💱 Exchange Rate: 1 INR = ${INR_TO_USD_RATE} USD")
    print("✨ Ready to serve predictions!")
    demo.launch()
