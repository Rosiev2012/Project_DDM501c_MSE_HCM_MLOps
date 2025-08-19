"""
API Service cho ML Model Classification
=====================================
API endpoints để sử dụng mô hình đã train
"""

import joblib
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS cho frontend

# Global variables cho model
model = None
scaler = None
model_info = None

def load_model():
    """Load mô hình và scaler đã lưu"""
    global model, scaler, model_info
    
    try:
        model = joblib.load('models/best_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        
        with open('models/model_info.json', 'r') as f:
            model_info = json.load(f)
        
        logger.info(f"✅ Model loaded: {model_info['model_name']}")
        logger.info(f"📊 Accuracy: {model_info['accuracy']:.4f}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint để dự đoán phân loại
    Input: JSON {"features": [list of 10 numbers]}
    Output: JSON với prediction và probabilities
    """
    try:
        if model is None:
            return jsonify({
                "error": "Model not loaded", 
                "message": "Please ensure model files exist"
            }), 500
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        features = data.get('features')
        if not features:
            return jsonify({"error": "No features provided"}), 400
        
        # Validate số lượng features
        if len(features) != 10:
            return jsonify({
                "error": f"Expected 10 features, got {len(features)}"
            }), 400
        
        # Validate features là số
        try:
            features = [float(x) for x in features]
        except (ValueError, TypeError):
            return jsonify({"error": "All features must be numbers"}), 400
        
        # Chuẩn hóa và dự đoán
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        
        # Thực hiện dự đoán
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Trả về kết quả
        result = {
            "status": "success",
            "prediction": {
                "class": int(prediction),
                "label": f"Class {prediction}",
                "confidence": float(max(probabilities))
            },
            "probabilities": {
                "class_0": float(probabilities[0]),
                "class_1": float(probabilities[1])
            },
            "model_info": {
                "name": model_info['model_name'],
                "accuracy": model_info['accuracy'],
                "version": "1.0"
            }
        }
        
        logger.info(f"Prediction made: Class {prediction} (confidence: {max(probabilities):.3f})")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/model/info', methods=['GET'])
def model_info_api():
    """API để lấy thông tin mô hình"""
    if model_info is None:
        return jsonify({"error": "Model info not available"}), 500
    
    return jsonify({
        "status": "success",
        "model": model_info,
        "endpoints": {
            "predict": "/api/predict",
            "health": "/api/health",
            "info": "/api/model/info"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "timestamp": "2025-08-19T10:00:00Z",
        "version": "1.0"
    })

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    API endpoint để dự đoán nhiều mẫu cùng lúc
    Input: JSON {"samples": [[features], [features], ...]}
    """
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        data = request.get_json()
        samples = data.get('samples', [])
        
        if not samples:
            return jsonify({"error": "No samples provided"}), 400
        
        results = []
        for i, features in enumerate(samples):
            try:
                features = [float(x) for x in features]
                if len(features) != 10:
                    results.append({
                        "sample_id": i,
                        "error": f"Expected 10 features, got {len(features)}"
                    })
                    continue
                
                features_array = np.array(features).reshape(1, -1)
                features_scaled = scaler.transform(features_array)
                
                prediction = model.predict(features_scaled)[0]
                probabilities = model.predict_proba(features_scaled)[0]
                
                results.append({
                    "sample_id": i,
                    "prediction": int(prediction),
                    "confidence": float(max(probabilities)),
                    "probabilities": {
                        "class_0": float(probabilities[0]),
                        "class_1": float(probabilities[1])
                    }
                })
                
            except Exception as e:
                results.append({
                    "sample_id": i,
                    "error": str(e)
                })
        
        return jsonify({
            "status": "success",
            "results": results,
            "total_samples": len(samples)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/api/predict",
            "/api/batch-predict", 
            "/api/model/info",
            "/api/health"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Please check server logs"
    }), 500

if __name__ == "__main__":
    print("="*60)
    print("🚀 ML MODEL API SERVICE")
    print("="*60)
    
    # Load model
    if load_model():
        print("✅ Model loaded successfully")
        print("🌐 Starting API server...")
        print("📱 API Base URL: http://127.0.0.1:8000/api")
        print("🔗 Endpoints:")
        print("   - POST /api/predict")
        print("   - POST /api/batch-predict")
        print("   - GET  /api/model/info")
        print("   - GET  /api/health")
        print("="*60)
        
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        print("❌ Failed to load model. Please run ml_pipeline.py first!")
