"""
Flask Web Application for ML Model Prediction
============================================
"""

import joblib
import json
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load model and scaler
try:
    model = joblib.load('models/best_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    
    with open('models/model_info.json', 'r') as f:
        model_info = json.load(f)
    
    print("✅ Model loaded successfully!")
    print(f"📊 Model: {model_info['model_name']}")
    print(f"📈 Accuracy: {model_info['accuracy']:.4f}")
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    scaler = None
    model_info = {"model_name": "Unknown", "accuracy": 0.0}


@app.route('/')
def home():
    """Home page with prediction form"""
    return render_template('index.html', model_info=model_info)


@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    try:
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please run ml_pipeline.py first.'
            }), 500
        
        # Get data from request (10 features)
        data = request.get_json()
        features = [
            float(data['feature_0']),
            float(data['feature_1']),
            float(data['feature_2']),
            float(data['feature_3']),
            float(data['feature_4']),
            float(data['feature_5']),
            float(data['feature_6']),
            float(data['feature_7']),
            float(data['feature_8']),
            float(data['feature_9'])
        ]
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        # Binary classification (0 or 1)
        class_name = f"Class {prediction}"
        confidence = float(max(probability))
        
        return jsonify({
            'success': True,
            'prediction': class_name,
            'confidence': confidence,
            'probabilities': {
                'class_0': float(probability[0]),
                'class_1': float(probability[1])
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Alternative API endpoint"""
    return predict()


@app.route('/model-info')
def model_info_endpoint():
    """Get model information"""
    return jsonify(model_info)


@app.route('/health')
def health():
    """Health check endpoint"""
    status = "healthy" if model is not None else "unhealthy"
    return jsonify({"status": status, "model_loaded": model is not None})


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌐 STARTING FLASK WEB APPLICATION")
    print("="*50)
    print("📱 URL: http://127.0.0.1:5001")
    print("🔗 API: http://127.0.0.1:5001/predict")
    print("ℹ️  Info: http://127.0.0.1:5001/model-info")
    print("❤️  Health: http://127.0.0.1:5001/health")
    print("="*50)
    
    try:
        print("🚀 Starting Flask server...")
        app.run(debug=False, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"❌ Flask error: {e}")
        import traceback
        traceback.print_exc()
