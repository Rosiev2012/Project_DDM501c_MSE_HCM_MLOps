# 🚀 Dự án MLOps: Phân loại nhị phân với Machine Learning

## 📖 Mô tả dự án

Dự án này thực hiện đầy đủ pipeline MLOps từ việc tạo mô hình machine learning đến deploy web application, bao gồm:

1. **Tạo mô hình phân loại đơn giản nhất** (Logistic Regression)
2. **Thử nghiệm tuning siêu tham số** cho nhiều mô hình
3. **So sánh kết quả các mô hình** (Logistic Regression, Random Forest, XGBoost)
4. **Lưu mô hình tốt nhất** vào model registry
5. **Tạo ứng dụng web Flask** để sử dụng mô hình

## 🏗️ Cấu trúc dự án

```
ML_Tutorial/
├── ml_pipeline.py          # Code ML chính (training & evaluation)
├── app.py                  # Flask web application
├── requirements.txt        # Dependencies
├── README.md              # File này
├── templates/
│   └── index.html         # Giao diện web
└── models/                # Thư mục lưu mô hình
    ├── best_model.pkl     # Mô hình tốt nhất
    ├── scaler.pkl         # Scaler để chuẩn hóa dữ liệu
    └── model_info.json    # Thông tin mô hình
```

## 🔧 Cài đặt và chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy pipeline ML (Training mô hình)

```bash
python ml_pipeline.py
```

Kết quả sẽ hiển thị:
- ✅ So sánh các mô hình
- 🏆 Mô hình tốt nhất được chọn
- 💾 Mô hình được lưu vào thư mục `models/`

### 3. Chạy Flask web app

```bash
python app.py
```

Truy cập: **http://127.0.0.1:5000**

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

### POST /predict
Dự đoán phân loại
```json
{
  "features": [1.5, -0.8, 2.1, 0.3, -1.2, 0.9, 1.8, -0.5, 0.7, 1.1]
}
```

Response:
```json
{
  "prediction": 1,
  "prediction_label": "Lớp 1",
  "probability": {
    "class_0": 0.23,
    "class_1": 0.77
  },
  "confidence": 0.77,
  "model_info": {
    "name": "XGBoost",
    "accuracy": 0.8467
  }
}
```

### GET /model-info
Lấy thông tin mô hình
```json
{
  "model_name": "XGBoost",
  "accuracy": 0.8467,
  "features": 10,
  "training_samples": 1400
}
```

### GET /health
Health check
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

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

## 🔮 Mở rộng trong tương lai

- [ ] Thêm MLflow tracking
- [ ] Implement model versioning
- [ ] Add data drift detection
- [ ] Deploy lên cloud (AWS/GCP)
- [ ] Containerize với Docker
- [ ] CI/CD pipeline
- [ ] Model monitoring dashboard

## 👥 Tác giả

Dự án demo MLOps pipeline hoàn chỉnh

## 📝 License

MIT License
