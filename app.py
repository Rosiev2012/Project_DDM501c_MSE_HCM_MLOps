"""
Flask Web Application cho ML Model Prediction
===========================================
Ứng dụng web sử dụng mô hình ML tốt nhất để dự đoán
"""

import joblib
import json
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Tải mô hình và scaler đã lưu
try:
    model = joblib.load('models/best_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    
    # Tải thông tin mô hình
    with open('models/model_info.json', 'r') as f:
        model_info = json.load(f)
    
    print("✅ Đã tải mô hình thành công!")
    print(f"📊 Mô hình: {model_info['model_name']}")
    print(f"📈 Độ chính xác: {model_info['accuracy']:.4f}")
    
except Exception as e:
    print(f"❌ Lỗi khi tải mô hình: {e}")
    print("💡 Hãy chạy ml_pipeline.py trước!")
    model = None
    scaler = None
    model_info = None

@app.route('/')
def home():
    """Trang chủ hiển thị giao diện dự đoán"""
    return render_template('index.html', model_info=model_info)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint để thực hiện dự đoán"""
    try:
        if model is None:
            return jsonify({
                "error": "Mô hình chưa được tải. Vui lòng chạy ml_pipeline.py trước!"
            }), 500
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        features = data.get('features')
        
        if not features:
            return jsonify({"error": "Không có dữ liệu đầu vào"}), 400
        
        # Kiểm tra số lượng features
        if len(features) != model_info['features']:
            return jsonify({
                "error": f"Cần {model_info['features']} đặc trưng, nhận được {len(features)}"
            }), 400
        
        # Chuyển đổi và chuẩn hóa dữ liệu
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        
        # Thực hiện dự đoán
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        # Trả về kết quả
        result = {
            "prediction": int(prediction),
            "prediction_label": "Lớp 1" if prediction == 1 else "Lớp 0",
            "probability": {
                "class_0": float(probability[0]),
                "class_1": float(probability[1])
            },
            "confidence": float(max(probability)),
            "model_info": {
                "name": model_info['model_name'],
                "accuracy": model_info['accuracy']
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Lỗi dự đoán: {str(e)}"}), 500

@app.route('/model-info')
def get_model_info():
    """API endpoint để lấy thông tin mô hình"""
    if model_info is None:
        return jsonify({"error": "Thông tin mô hình không có sẵn"}), 500
    
    return jsonify(model_info)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = "healthy" if model is not None else "unhealthy"
    return jsonify({"status": status, "model_loaded": model is not None})

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌐 KHỞI ĐỘNG FLASK WEB APPLICATION")
    print("="*50)
    print("📱 Truy cập: http://127.0.0.1:5001")
    print("🔗 API: http://127.0.0.1:5001/predict")
    print("ℹ️  Info: http://127.0.0.1:5001/model-info")
    print("❤️  Health: http://127.0.0.1:5001/health")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
