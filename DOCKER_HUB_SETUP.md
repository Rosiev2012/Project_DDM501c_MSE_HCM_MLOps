# 🐳 Docker Hub Auto-Deploy Setup Guide

## 📋 Current CI/CD Docker Integration

✅ **CI/CD đã được config để auto-push lên Docker Hub!**

### 🔧 Setup Required:

#### 1. **GitHub Repository Variables:**
Go to: `Settings` → `Variables and secrets` → `Actions` → `Variables`

Add variable:
```
Name: DOCKERHUB_USERNAME
Value: your-dockerhub-username
```

#### 2. **GitHub Repository Secrets:**
Go to: `Settings` → `Variables and secrets` → `Actions` → `Secrets`

Add secret:
```
Name: DOCKERHUB_TOKEN
Value: your-dockerhub-access-token
```

**Tạo Docker Hub Access Token:**
1. Login Docker Hub → Account Settings
2. Security → Access Tokens  
3. New Access Token → Read, Write, Delete permissions
4. Copy token và paste vào GitHub secret

---

## 🚀 Auto-Deploy Behavior

### ✅ **Khi push to master:**
- Build Docker image
- Tag: `ml-model-api:latest` 
- Push to: `{DOCKERHUB_USERNAME}/ml-model-api:latest`
- Available at: `docker pull {username}/ml-model-api:latest`

### 🔄 **Khi push to PR/branch khác:**
- Build Docker image locally only
- Test container functionality  
- **NO push to Docker Hub**

---

## 📦 Docker Commands After Setup

```bash
# Pull latest from Docker Hub
docker pull {your-username}/ml-model-api:latest

# Run container  
docker run -p 5001:5001 {your-username}/ml-model-api:latest

# Check web app
curl http://localhost:5001/health
```

---

## 🎯 Current Status

**Without Docker Hub credentials:**
- ✅ Build succeeds
- ✅ Local testing works
- ❌ No push to Docker Hub

**With Docker Hub credentials:**
- ✅ Build succeeds  
- ✅ Auto-push to Docker Hub
- ✅ Public image available
- ✅ Can deploy anywhere with `docker pull`

---

Setup these credentials để enable auto-push!
✅ Docker Hub Auto-Deploy Configured
