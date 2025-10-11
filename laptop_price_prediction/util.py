import json
import pickle
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Global variables to store loaded data
__companies = None
__type_names = None
__cpu_brands = None
__gpu_brands = None
__os_types = None
__numerical_features = None
__model = None
__scaler = None
__columns = None

def load_saved_artifacts():
    """Load model, scaler, and feature columns from artifacts"""
    print("Loading saved artifacts...")
    global __companies, __type_names, __cpu_brands, __gpu_brands, __os_types
    global __numerical_features, __model, __scaler, __columns
    
    # Load feature columns
    with open(r"C:\Users\Abeycity\Desktop\data science\laptop website\input_columns.json", "r") as f:

        all_columns = json.load(f)
        __columns = all_columns
        
        # Extract different categories and remove prefixes
        __companies = [col.replace("Company_", "") for col in all_columns if col.startswith("Company_")]
        __type_names = [col.replace("TypeName_", "") for col in all_columns if col.startswith("TypeName_")]
        __cpu_brands = [col.replace("Cpu brand_", "") for col in all_columns if col.startswith("Cpu brand_")]
        __gpu_brands = [col.replace("Gpu brand_", "") for col in all_columns if col.startswith("Gpu brand_")]
        __os_types = [col.replace("os_", "") for col in all_columns if col.startswith("os_")]
        
        # Extract numerical features
        prefixed_columns = ["Company_", "TypeName_", "Cpu brand_", "Gpu brand_", "os_"]
        __numerical_features = [col for col in all_columns if not any(col.startswith(prefix) for prefix in prefixed_columns)]
    
    # Load model
    import joblib
    __model = joblib.load(r"C:\Users\Abeycity\Desktop\data science\laptop website\artifacts\best_model.pkl")
    
    # Try to load scaler
    try:
        with open(r"C:\Users\Abeycity\Desktop\data science\laptop website\scaler.pkl", 'rb') as f:
            __scaler = pickle.load(f)
        print("Scaler loaded successfully")
    except FileNotFoundError:
        print("Warning: scaler.pkl not found. Numeric features won't be scaled.")
        __scaler = None
    
    print("Loading saved artifacts...done")

def get_company_names():
    return __companies

def get_type_names():
    return __type_names

def get_cpu_brands():
    return __cpu_brands

def get_gpu_brands():
    return __gpu_brands

def get_os_types():
    return __os_types

def get_numerical_features():
    return __numerical_features

def get_model():
    return __model

def predict_price(model, laptop_features, columns):
    """Your original prediction function"""
    # Create a DataFrame from the input features
    features_df = pd.DataFrame([laptop_features])

    # One-Hot Encode categorical features
    categorical_cols = ['Company', 'TypeName', 'Cpu brand', 'Gpu brand', 'os']
    features_df = pd.get_dummies(features_df, columns=categorical_cols, drop_first=True, dtype=int)

    # Ensure the columns match the training data, adding missing columns with 0
    for col in columns:
        if col not in features_df.columns:
            features_df[col] = 0

    # Reorder columns to match the training data
    features_df = features_df[columns]

    # Scale numeric features using the same scaler as the training data
    numeric_cols = ['Ram', 'Total_Storage']
    if __scaler is not None:
        features_df[numeric_cols] = __scaler.transform(features_df[numeric_cols])
    else:
        print("Warning: No scaler available. Using raw numeric values.")

    # Drop the 'Price' column if it exists
    if 'Price' in features_df.columns:
        features_df = features_df.drop(columns=['Price'])

    # Drop the 'index' column as it was dropped from X
    if 'index' in features_df.columns:
        features_df = features_df.drop(columns=['index'])

    # Make prediction
    predicted_price = model.predict(features_df)
    return predicted_price[0]

def get_estimated_price(company, ram, touchscreen, ips, total_storage, type_name, cpu_brand, gpu_brand, os_type):
    """Get estimated price using your prediction function"""
    if __model is None or __columns is None:
        print("Model or columns not loaded. Call load_saved_artifacts() first.")
        return None
    
    try:
        # Create laptop features dictionary
        laptop_features = {
            'Company': company,
            'Ram': ram,
            'Touchscreen': touchscreen,
            'Ips': ips,
            'Total_Storage': total_storage,
            'TypeName': type_name,
            'Cpu brand': cpu_brand,
            'Gpu brand': gpu_brand,
            'os': os_type
        }
        
        # Use your original prediction function
        estimated_price = predict_price(__model, laptop_features, __columns)
        estimated_price = round(estimated_price, 2)
        
        print(f"Estimated price for {company} laptop: ${estimated_price}")
        return estimated_price
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

def validate_inputs(company, type_name, cpu_brand, gpu_brand, os_type):
    """Validate input values"""
    validation = {'valid': True, 'errors': []}
    
    if company not in __companies:
        validation['valid'] = False
        validation['errors'].append(f"Company '{company}' not found. Available: {__companies}")
    
    if type_name not in __type_names:
        validation['valid'] = False
        validation['errors'].append(f"Type '{type_name}' not found. Available: {__type_names}")
    
    if cpu_brand not in __cpu_brands:
        validation['valid'] = False
        validation['errors'].append(f"CPU brand '{cpu_brand}' not found. Available: {__cpu_brands}")
    
    if gpu_brand not in __gpu_brands:
        validation['valid'] = False
        validation['errors'].append(f"GPU brand '{gpu_brand}' not found. Available: {__gpu_brands}")
    
    if os_type not in __os_types:
        validation['valid'] = False
        validation['errors'].append(f"OS type '{os_type}' not found. Available: {__os_types}")
    
    return validation

if __name__ == '__main__':
    load_saved_artifacts()
    print("\n=== Available Options ===")
    print(f"Companies: {get_company_names()}")
    print(f"Laptop Types: {get_type_names()}")
    print(f"CPU Brands: {get_cpu_brands()}")
    print(f"GPU Brands: {get_gpu_brands()}")
    print(f"Operating Systems: {get_os_types()}")
    print(f"Numerical Features: {get_numerical_features()}")
    print(f"Model loaded: {__model is not None}")
    
    # Test prediction
    print("\n=== Test Prediction ===")
    if __companies and __type_names and __cpu_brands and __gpu_brands and __os_types:
        test_price = get_estimated_price(
            company=__companies[0],  # First available company
            ram=8,
            touchscreen=1,
            ips=1,
            total_storage=256,
            type_name=__type_names[0],  # First available type
            cpu_brand=__cpu_brands[0],  # First available CPU
            gpu_brand=__gpu_brands[0],  # First available GPU
            os_type=__os_types[0]  # First available OS
        )