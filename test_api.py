"""
API Request Client - Test ML Model API
====================================
Script để test các API endpoints của ML model
"""

import requests
import json
import numpy as np
import time

# Cấu hình API
API_BASE_URL = "http://127.0.0.1:8000/api"
WEB_APP_URL = "http://127.0.0.1:5001"

class MLModelClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """Kiểm tra trạng thái API"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_model_info(self):
        """Lấy thông tin mô hình"""
        try:
            response = self.session.get(f"{self.base_url}/model/info")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def predict_single(self, features):
        """Dự đoán một mẫu"""
        try:
            data = {"features": features}
            response = self.session.post(
                f"{self.base_url}/predict",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def predict_batch(self, samples):
        """Dự đoán nhiều mẫu"""
        try:
            data = {"samples": samples}
            response = self.session.post(
                f"{self.base_url}/batch-predict",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def generate_sample_data(n_samples=1):
    """Tạo dữ liệu mẫu để test"""
    samples = []
    for _ in range(n_samples):
        # Tạo 10 features ngẫu nhiên
        features = [round(np.random.normal(0, 1), 3) for _ in range(10)]
        samples.append(features)
    return samples

def test_api_endpoints():
    """Test tất cả API endpoints"""
    print("🚀 TESTING ML MODEL API")
    print("="*50)
    
    client = MLModelClient()
    
    # 1. Health Check
    print("\n1️⃣ Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    if health.get("status") != "healthy":
        print("❌ API không hoạt động. Hãy khởi động api_service.py trước!")
        return
    
    # 2. Model Info
    print("\n2️⃣ Model Info:")
    model_info = client.get_model_info()
    print(json.dumps(model_info, indent=2))
    
    # 3. Single Prediction
    print("\n3️⃣ Single Prediction:")
    sample_features = generate_sample_data(1)[0]
    print(f"Input features: {sample_features}")
    
    prediction = client.predict_single(sample_features)
    print("Result:")
    print(json.dumps(prediction, indent=2))
    
    # 4. Batch Prediction
    print("\n4️⃣ Batch Prediction:")
    batch_samples = generate_sample_data(3)
    print(f"Input samples: {len(batch_samples)} samples")
    
    batch_result = client.predict_batch(batch_samples)
    print("Result:")
    print(json.dumps(batch_result, indent=2))
    
    # 5. Error Testing
    print("\n5️⃣ Error Testing:")
    print("Testing with invalid features...")
    invalid_features = [1, 2, 3]  # Chỉ 3 features thay vì 10
    error_result = client.predict_single(invalid_features)
    print(json.dumps(error_result, indent=2))

def test_web_app_api():
    """Test Web App API"""
    print("\n🌐 TESTING WEB APP API")
    print("="*50)
    
    try:
        # Test web app predict endpoint
        sample_features = generate_sample_data(1)[0]
        
        response = requests.post(
            f"{WEB_APP_URL}/predict",
            json={"features": sample_features},
            headers={"Content-Type": "application/json"}
        )
        
        print("Web App Prediction:")
        print(json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f"❌ Lỗi kết nối Web App: {e}")

def performance_test():
    """Test hiệu suất API"""
    print("\n⚡ PERFORMANCE TEST")
    print("="*50)
    
    client = MLModelClient()
    n_requests = 10
    
    # Tạo dữ liệu test
    test_samples = generate_sample_data(n_requests)
    
    # Test single predictions
    print(f"Testing {n_requests} single predictions...")
    start_time = time.time()
    
    for i, features in enumerate(test_samples):
        result = client.predict_single(features)
        if "error" in result:
            print(f"❌ Request {i+1} failed: {result['error']}")
        else:
            print(f"✅ Request {i+1}: Class {result['prediction']['class']}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n📊 Performance Results:")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per request: {total_time/n_requests:.3f} seconds")
    print(f"Requests per second: {n_requests/total_time:.2f}")

def load_test():
    """Test tải của API"""
    print("\n🔥 LOAD TEST")
    print("="*50)
    
    client = MLModelClient()
    
    # Test batch prediction với nhiều samples
    batch_sizes = [1, 5, 10, 20]
    
    for batch_size in batch_sizes:
        print(f"\nTesting batch size: {batch_size}")
        test_samples = generate_sample_data(batch_size)
        
        start_time = time.time()
        result = client.predict_batch(test_samples)
        end_time = time.time()
        
        if "error" in result:
            print(f"❌ Batch failed: {result['error']}")
        else:
            processing_time = end_time - start_time
            print(f"✅ Processed {batch_size} samples in {processing_time:.3f}s")
            print(f"📊 Throughput: {batch_size/processing_time:.2f} samples/second")

if __name__ == "__main__":
    print("🧪 ML MODEL API TESTING SUITE")
    print("="*60)
    
    try:
        # Test cơ bản
        test_api_endpoints()
        
        # Test web app
        test_web_app_api()
        
        # Test hiệu suất
        performance_test()
        
        # Test tải
        load_test()
        
        print("\n✅ Testing completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Testing stopped by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")

# Ví dụ sử dụng trực tiếp
def example_usage():
    """Ví dụ sử dụng client"""
    
    # Khởi tạo client
    client = MLModelClient()
    
    # Kiểm tra health
    health = client.health_check()
    print("Health:", health)
    
    # Dự đoán một mẫu
    features = [1.2, -0.5, 0.8, 1.1, -0.3, 0.9, -1.2, 0.4, 1.5, -0.7]
    result = client.predict_single(features)
    print("Prediction:", result)
    
    # Dự đoán nhiều mẫu
    samples = generate_sample_data(3)
    batch_result = client.predict_batch(samples)
    print("Batch prediction:", batch_result)
