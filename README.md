# 🚀 Dự án MLOps: Phân loại nhị phân với Machine Learning

## 📖 Mô tả dự án

Dự án MLOps hoàn chỉnh thực hiện classification task với đầy đủ pipeline production-ready, bao gồm:

### **🎯 Machine Learning Pipeline:**
1. **Data Generation**: Synthetic dataset với `make_classification`
2. **Model Training**: 5 models (Logistic Regression, LR-tuned, Random Forest, RF-tuned, XGBoost)
3. **Hyperparameter Tuning**: GridSearchCV cho optimization
4. **Model Evaluation**: Comprehensive metrics (accuracy, precision, recall, f1-score)
5. **Model Selection**: Automatic best model selection (XGBoost ~86.5% accuracy)
6. **Model Persistence**: Serialization với joblib

### **🌐 API & Web Services:**
7. **RESTful API**: Production-ready với Flask, CORS, logging
8. **Web Application**: Interactive UI cho predictions
9. **API Testing**: Comprehensive test suite với performance benchmarks

### **🚀 DevOps & Deployment:**
10. **Docker Containerization**: Multi-stage builds cho optimization
11. **CI/CD Pipeline**: GitHub Actions với automated testing & deployment
12. **Documentation**: Complete setup và workflow guides

### **🏆 Kết quả đạt được:**
- ✅ **Best Model**: XGBoost với 86.5% accuracy
- ✅ **Production API**: RESTful service với health checks
- ✅ **Web Interface**: User-friendly prediction interface  
- ✅ **Docker Ready**: Containerized cho scalable deployment
- ✅ **CI/CD Pipeline**: Automated testing và deployment workflow

## 🏗️ Cấu trúc dự án

```
Project_DDM501c_MSE_HCM_MLOps/
├── .github/workflows/
│   └── ci-cd.yml              # GitHub Actions CI/CD pipeline
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker container configuration
├── README.md                  # Tài liệu dự án (file này)
├── SETUP_GUIDE.md            # Hướng dẫn cài đặt chi tiết
├── WORKFLOW_GUIDE.md         # Hướng dẫn workflow MLOps
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker orchestration
├── 
├── 🧠 ML Core Files:
├── ml_pipeline.py            # ML training pipeline (XGBoost, RF, LR)
├── models/                   # Trained models directory
│   ├── best_model.pkl       # Best model (XGBoost ~86.5% accuracy)
│   ├── scaler.pkl          # Data preprocessing scaler
│   └── model_info.json     # Model metadata & performance
├── 
├── 🌐 API & Web Services:
├── api_service.py           # RESTful API service (port 8000)
├── app.py                   # Flask web application (port 5001)
├── test_api.py             # API testing & client
├── templates/
│   └── index.html          # Web UI for predictions
├── 
├── 🚀 Deployment & Scripts:
├── deploy_local.sh         # Local deployment script
└── run_project.sh          # Complete project runner
```

### 📂 **Mô tả từng thành phần:**

#### **🧠 ML Core**
- **`ml_pipeline.py`**: Complete ML pipeline với 5 models (LR, LR-tuned, RF, RF-tuned, XGBoost)
- **`models/`**: Lưu trữ trained models và metadata

#### **🌐 Services**  
- **`api_service.py`**: Production-ready API với CORS, logging, error handling
- **`app.py`**: Web interface cho end-users
- **`test_api.py`**: Comprehensive API testing suite

#### **🚀 DevOps**
- **`Dockerfile`**: Multi-stage build cho production deployment
- **`docker-compose.yml`**: Orchestration cho development environment  
- **`.github/workflows/ci-cd.yml`**: Automated testing, building, và deployment

#### **📖 Documentation**
- **`README.md`**: Project overview và quick start
- **`SETUP_GUIDE.md`**: Detailed setup instructions
- **`WORKFLOW_GUIDE.md`**: MLOps workflow explanation

## 🔧 Cài đặt và chạy

### **🚀 Quick Start (Recommended)**

```bash
# 1. Clone repository
git clone https://github.com/Rosiev2012/Project_DDM501c_MSE_HCM_MLOps.git
cd Project_DDM501c_MSE_HCM_MLOps

# 2. Run complete project
chmod +x run_project.sh
./run_project.sh
```

### **🐳 Docker Deployment (Production)**

```bash
# Build và run với Docker
docker build -t ml-model-api:v1.0 .
docker run -p 8000:8000 --name ml-api \
  ml-model-api:v1.0 bash -c "python ml_pipeline.py && python api_service.py"

# Hoặc sử dụng docker-compose
docker-compose up -d
```

### **💻 Manual Setup (Development)**

#### 1. Setup Environment
```bash
# Tạo virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

#### 2. Train Models
```bash
python ml_pipeline.py
```
**Output:**
- ✅ So sánh 5 mô hình (LR, LR-tuned, RF, RF-tuned, XGBoost)
- 🏆 Best model: XGBoost (~86.5% accuracy)
- 💾 Models saved to `models/` directory

#### 3. Start API Service
```bash
python api_service.py
```
**Access:** http://127.0.0.1:8000

**API Endpoints:**
- `GET /api/health` - Health check
- `POST /api/predict` - Single prediction
- `POST /api/batch-predict` - Batch predictions
- `GET /api/model/info` - Model information

#### 4. Start Web Application
```bash
python app.py
```
**Access:** http://127.0.0.1:5001

**Features:**
- 🎯 Interactive prediction interface
- 📊 Real-time probability visualization
- 🎲 Random data generation for testing
- 📱 Responsive design

#### 5. Run API Tests
```bash
python test_api.py
```
**Includes:**
- ✅ Health checks
- ✅ Single & batch predictions
- ✅ Performance benchmarks
- ✅ Load testing

## 📊 Kết quả mô hình

| Mô hình | Accuracy | Đặc điểm |
|---------|----------|----------|
| Logistic Regression | ~72% | Đơn giản, nhanh |
| Random Forest (tuned) | ~84% | Cân bằng hiệu suất/tốc độ |
| XGBoost | ~85% | Tốt nhất, chậm hơn |

## 🌐 Web Application Features

- 🎯 **Dự đoán realtime**: Nhập 10 đặc trưng và nhận kết quả ngay lập tức
- 📊 **Hiển thị xác suất**: Xem xác suất từng lớp (0 và 1)
- 🎲 **Tạo dữ liệu mẫu**: Generate random data để test
- 📱 **Responsive UI**: Giao diện đẹp, tương thích mobile
- ℹ️ **Thông tin mô hình**: Hiển thị accuracy và metadata

## 🔌 API Endpoints

### **🎯 API Service (Port 8000)**

#### **POST /api/predict**
Single prediction endpoint
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.5, -0.8, 2.1, 0.3, -1.2, 0.9, 1.8, -0.5, 0.7, 1.1]}'
```

**Response:**
```json
{
  "status": "success",
  "prediction": {
    "class": 1,
    "label": "Class 1", 
    "confidence": 0.87
  },
  "probabilities": {
    "class_0": 0.13,
    "class_1": 0.87
  },
  "model_info": {
    "name": "XGBoost",
    "accuracy": 0.865,
    "version": "1.0"
  }
}
```

#### **POST /api/batch-predict**
Batch prediction cho multiple samples
```bash
curl -X POST http://localhost:8000/api/batch-predict \
  -H "Content-Type: application/json" \
  -d '{"samples": [[1,2,3,4,5,6,7,8,9,0], [0,1,2,3,4,5,6,7,8,9]]}'
```

#### **GET /api/health**
Health check endpoint
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-08-19T10:00:00Z",
  "version": "1.0"
}
```

#### **GET /api/model/info**
Model information và metadata
```json
{
  "status": "success",
  "model": {
    "model_name": "XGBoost",
    "accuracy": 0.865,
    "features": 10,
    "training_samples": 1400
  },
  "endpoints": {
    "predict": "/api/predict",
    "health": "/api/health",
    "info": "/api/model/info"
  }
}
```

### **🌐 Web Application (Port 5001)**

#### **POST /predict**
Web app prediction endpoint
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.5, -0.8, 2.1, 0.3, -1.2, 0.9, 1.8, -0.5, 0.7, 1.1]}'
```

#### **GET /model-info**
Web app model information

#### **GET /health** 
Web app health check

## 🎯 Hướng dẫn sử dụng từng bước

### Bước 1: Tạo mô hình đơn giản
```python
# Logistic Regression - mô hình cơ bản nhất
simple_model = LogisticRegression(random_state=42)
simple_model.fit(X_train, y_train)
```

### Bước 2: Tuning siêu tham số
```python
# GridSearchCV cho Logistic Regression
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'lbfgs'],
    'max_iter': [100, 200, 500]
}
grid_search = GridSearchCV(model, param_grid, cv=5)
```

### Bước 3: So sánh mô hình
- Logistic Regression: Baseline
- Random Forest: Ensemble method
- XGBoost: Gradient boosting

### Bước 4: Lưu mô hình tốt nhất
```python
# Lưu mô hình, scaler và metadata
joblib.dump(best_model, 'models/best_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
```

### Bước 5: Deploy web app
```python
# Flask app load mô hình và serve predictions
app = Flask(__name__)
model = joblib.load('models/best_model.pkl')
```

## 🚨 Troubleshooting

### Lỗi "Mô hình chưa được tải"
- Chạy `python ml_pipeline.py` trước để tạo mô hình

### Lỗi thiếu dependencies
- Chạy `pip install -r requirements.txt`

### Port 5000 đã được sử dụng
- Đổi port trong `app.py`: `app.run(port=5001)`

## 🔄 Workflow hoàn chỉnh

1. **Data Generation** → Tạo synthetic data
2. **Model Training** → Train multiple models
3. **Hyperparameter Tuning** → GridSearchCV
4. **Model Evaluation** → Compare metrics
5. **Model Selection** → Choose best model
6. **Model Saving** → Serialize to disk
7. **Web Deployment** → Flask REST API
8. **User Interface** → Interactive web app

## 📈 Metrics được sử dụng

- **Accuracy**: Độ chính xác tổng thể
- **Precision**: Độ chính xác từng lớp
- **Recall**: Độ nhạy từng lớp  
- **F1-Score**: Trung bình hài hòa P&R
- **Confusion Matrix**: Ma trận nhầm lẫn

## 👥 Tác giả
Nguyễn Thị Hồng Nhung
