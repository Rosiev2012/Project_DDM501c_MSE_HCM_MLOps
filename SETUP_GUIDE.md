# 🔧 Setup GitLab và DockerHub cho CI/CD

## 📋 Checklist Setup

### 1. Tạo account GitLab
- [ ] Đăng ký tại: https://gitlab.com
- [ ] Verify email
- [ ] Tạo repository mới cho dự án

### 2. Tạo account DockerHub  
- [ ] Đăng ký tại: https://hub.docker.com
- [ ] Verify email
- [ ] Tạo repository public: `username/ml-model-api`

### 3. Lấy credentials và tokens

#### GitLab Personal Access Token:
1. Vào GitLab → Settings → Access Tokens
2. Tạo token với scopes:
   - [x] api
   - [x] read_repository
   - [x] write_repository
3. Copy token (chỉ hiện 1 lần!)

#### DockerHub Access Token:
1. Vào DockerHub → Account Settings → Security
2. New Access Token
3. Copy token

### 4. Cấu hình CI/CD Variables trong GitLab

Vào Project → Settings → CI/CD → Variables, thêm:

| Key | Value | Protected | Masked |
|-----|-------|-----------|--------|
| `DOCKER_USERNAME` | your-dockerhub-username | ✅ | ❌ |
| `DOCKER_PASSWORD` | your-dockerhub-token | ✅ | ✅ |
| `CI_REGISTRY_USER` | your-dockerhub-username | ❌ | ❌ |

## 🚀 Các bước thực hiện

### Bước 1: Clone và push code lên GitLab

```bash
# Khởi tạo git repository
cd /Users/rose/Desktop/MSE22HCM/DevOps/Project_DDM501c_MSE.HCM.SU25.Nguyen_Thi_Hong_Nhung
git init
git add .
git commit -m "Initial commit: ML Model API with CI/CD"

# Thêm GitLab remote
git remote add origin https://gitlab.com/YOUR_USERNAME/ml-model-api.git

# Push lên GitLab
git branch -M main
git push -u origin main
```

### Bước 2: Test CI/CD Pipeline

1. **Trigger Pipeline:**
   - Mỗi khi push code sẽ trigger pipeline
   - Hoặc vào GitLab → CI/CD → Pipelines → Run Pipeline

2. **Kiểm tra các stages:**
   - ✅ Test: Chạy ML pipeline, API tests
   - ✅ Build: Build Docker image
   - ✅ Deploy: Deploy (manual cho production)

### Bước 3: Test Docker build local

```bash
# Build image
docker build -t ml-model-api:local .

# Run container
docker run -p 8000:8000 ml-model-api:local

# Test API
curl http://localhost:8000/api/health
```

### Bước 4: Test với Docker Compose

```bash
# Đảm bảo có trained models
python ml_pipeline.py

# Start all services
docker-compose up -d

# Check services
docker-compose ps

# Test API
curl http://localhost:8000/api/health
curl http://localhost:5001/health

# View logs
docker-compose logs -f ml-api

# Stop services
docker-compose down
```

## 🔐 Security Best Practices

### GitLab CI/CD Variables:
- ✅ Mask sensitive values (tokens, passwords)
- ✅ Protect variables for main branches only
- ✅ Use separate tokens for different environments

### Docker Security:
- ✅ Use non-root user trong container
- ✅ Multi-stage builds để minimize image size
- ✅ Scan images với security tools
- ✅ Use specific tags thay vì :latest

### API Security:
- ✅ Input validation
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Health checks

## 🐛 Troubleshooting

### Pipeline fails at build stage:
```bash
# Check GitLab Runner logs
# Verify Docker credentials
# Test Docker build locally
```

### API tests fail:
```bash
# Check if models exist
ls -la models/
python ml_pipeline.py

# Test API locally
python api_service.py
python test_api.py
```

### Docker image too large:
```bash
# Use multi-stage builds
# Remove unnecessary packages
# Use .dockerignore
```

## 📊 Monitoring và Logging

### GitLab CI/CD:
- Pipeline status dashboard
- Job logs và artifacts
- Performance metrics

### Docker:
- Container logs: `docker logs container_name`
- Resource usage: `docker stats`
- Health checks status

### API Monitoring:
- Health check endpoints
- Performance metrics
- Error tracking

## 🔄 Workflow Process

### Development:
1. Create feature branch
2. Make changes
3. Push → triggers pipeline
4. MR → triggers build without push
5. Merge → deploys to dev

### Production:
1. Merge to main
2. Pipeline builds và pushes image
3. Manual deployment to production
4. Monitoring và rollback nếu cần

## 📞 Support

### GitLab Issues:
- Check runner status
- Verify variables configuration
- Review pipeline logs

### DockerHub Issues:
- Verify credentials
- Check repository permissions
- Test docker login locally

### API Issues:
- Check model files
- Verify dependencies
- Test API endpoints locally
