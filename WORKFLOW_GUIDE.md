# CI/CD Workflow - Localhost Deployment
# ====================================

## 🔄 Complete Development Workflow

### 1. Development Phase
```bash
# Make changes to code
vim ml_pipeline.py

# Test locally
python ml_pipeline.py
python test_api.py

# Commit changes
git add .
git commit -m "Update: improve model accuracy"
```

### 2. CI/CD Pipeline (GitLab)
```bash
# Push triggers pipeline
git push origin main

# Pipeline stages:
# ✅ Test: Run all tests
# ✅ Build: Create Docker image  
# ✅ Push: Upload to DockerHub
```

### 3. Local Deployment
```bash
# Manual deployment
chmod +x deploy_local.sh
./deploy_local.sh

# Or use docker-compose directly
docker-compose down
docker-compose pull  # Pull latest images
docker-compose up -d
```

## 📋 Daily Workflow

### Morning Setup:
```bash
# Check if new deployment available
docker images | grep ml-model-api

# Deploy latest version
./deploy_local.sh
```

### Development:
```bash
# Work on features
git checkout -b feature/new-algorithm
# ... make changes ...
git commit -m "Add new algorithm"
git push origin feature/new-algorithm

# Create Merge Request on GitLab
# Pipeline runs automatically
```

### Deployment:
```bash
# After MR merged to main
git checkout main
git pull origin main

# Wait for pipeline to complete
# Check GitLab CI/CD status

# Deploy to localhost
./deploy_local.sh
```

## 🐛 Troubleshooting

### Pipeline fails:
```bash
# Check GitLab pipeline logs
# Fix issues locally first:
python ml_pipeline.py  # Test training
python test_api.py     # Test API
docker build -t test . # Test Docker build
```

### Deployment fails:
```bash
# Check Docker status
docker ps
docker-compose logs

# Manual recovery
docker-compose down
docker system prune -f
./deploy_local.sh
```

### Image not updating:
```bash
# Force pull new image
docker-compose down
docker rmi YOUR_USERNAME/ml-model-api:latest
docker-compose up -d
```

## 📊 Monitoring

### Check service status:
```bash
# Services status
docker-compose ps

# Logs
docker-compose logs -f ml-api

# Resource usage
docker stats
```

### API monitoring:
```bash
# Health checks
curl http://localhost:8000/api/health
curl http://localhost:5001/health

# Performance test
python test_api.py
```

## 🔧 Advanced Features

### Blue-Green Deployment:
```bash
# Run old version on port 8000
# Run new version on port 8001
# Switch traffic when ready
```

### Rollback:
```bash
# Use specific version
docker-compose down
docker run -d -p 8000:8000 YOUR_USERNAME/ml-model-api:v1.0
```

### Backup:
```bash
# Backup models
tar -czf models_backup.tar.gz models/

# Backup Docker images
docker save YOUR_USERNAME/ml-model-api:latest > ml-api-backup.tar
```

## 🎯 Success Criteria

✅ Code changes → Auto pipeline  
✅ Pipeline success → Image in DockerHub  
✅ One-command deployment to localhost  
✅ Health checks pass  
✅ Zero-downtime updates  
✅ Easy rollback capability  

## 📝 Notes

- **No external server needed** - Everything runs on localhost
- **GitLab CI/CD is free** - Up to 400 minutes/month
- **DockerHub is free** - 1 private repo + unlimited public
- **Perfect for learning** - Full DevOps experience locally
