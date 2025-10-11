from flask import Flask, request, jsonify, render_template
import util

app = Flask(__name__)

# Load artifacts when server starts
util.load_saved_artifacts()

# Current exchange rate (INR to USD)
# You can update this value or fetch it from an API for real-time rates
INR_TO_USD_RATE = 0.01171  # 1 INR = 0.01171 USD (as of Aug 2025)

def convert_inr_to_usd(inr_amount):
    """Convert Indian Rupees to US Dollars"""
    return round(inr_amount * INR_TO_USD_RATE, 2)

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/options')
def get_options():
    """Get all available options for dropdowns"""
    try:
        options = {
            'companies': util.get_company_names(),
            'type_names': util.get_type_names(),
            'cpu_brands': util.get_cpu_brands(),
            'gpu_brands': util.get_gpu_brands(),
            'os_types': util.get_os_types(),
            'numerical_features': util.get_numerical_features()
        }
        return jsonify(options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make price prediction"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company', 'ram', 'touchscreen', 'ips', 'total_storage', 
                          'type_name', 'cpu_brand', 'gpu_brand', 'os_type']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate inputs
        validation = util.validate_inputs(
            data['company'], 
            data['type_name'], 
            data['cpu_brand'], 
            data['gpu_brand'], 
            data['os_type']
        )
        
        if not validation['valid']:
            return jsonify({'error': 'Invalid inputs', 'details': validation['errors']}), 400
        
        # Make prediction (this returns price in INR)
        estimated_price_inr = util.get_estimated_price(
            company=data['company'],
            ram=int(data['ram']),
            touchscreen=int(data['touchscreen']),
            ips=int(data['ips']),
            total_storage=int(data['total_storage']),
            type_name=data['type_name'],
            cpu_brand=data['cpu_brand'],
            gpu_brand=data['gpu_brand'],
            os_type=data['os_type']
        )
        
        if estimated_price_inr is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        # Convert INR to USD
        estimated_price_usd = convert_inr_to_usd(estimated_price_inr)
        
        return jsonify({
            'estimated_price': estimated_price_usd,
            'estimated_price_inr': estimated_price_inr,
            'currency': 'USD',
            'exchange_rate': INR_TO_USD_RATE,
            'inputs': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'model_loaded': util.get_model() is not None,
        'exchange_rate_inr_to_usd': INR_TO_USD_RATE
    })

@app.route('/api/exchange-rate')
def get_exchange_rate():
    """Get current exchange rate"""
    return jsonify({
        'inr_to_usd': INR_TO_USD_RATE,
        'usd_to_inr': round(1 / INR_TO_USD_RATE, 2),
        'last_updated': 'August 2025'
    })

if __name__ == '__main__':
    print("🚀 Starting Laptop Price Prediction Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print(f"💱 Current Exchange Rate: 1 INR = ${INR_TO_USD_RATE} USD")
    print("📋 API Endpoints:")
    print("   GET  /                 : Main web interface")
    print("   GET  /api/options      : Get dropdown options")
    print("   POST /api/predict      : Make price prediction (converts INR to USD)")
    print("   GET  /api/health       : Health check")
    print("   GET  /api/exchange-rate: Get current exchange rate")
    print("✨ Ready to serve predictions!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)