# 🚀 Deployment Guide - Student Introduction Evaluator

## Overview
Complete step-by-step guide to deploy the Student Introduction Evaluator locally or on cloud platforms.

---

## 📋 Prerequisites

### Required Software
- **Python 3.9+** (recommended: 3.10 or 3.11)
- **pip** (Python package manager)
- **Git** (for cloning repository)
- **Java** (optional, for LanguageTool grammar checking)

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended for semantic models)
- **Disk Space**: ~2GB for models and dependencies
- **OS**: Windows, macOS, or Linux

---

## 🏠 Local Deployment (Development)

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/student-introduction-evaluator.git
cd student-introduction-evaluator

# Or if working locally
cd "/Users/ravishkumar/Desktop/Case Study"
```

### Step 2: Create Virtual Environment (Recommended)

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**This will install:**
- `vaderSentiment` - Sentiment analysis
- `language-tool-python` - Grammar checking
- `nltk` - NLP utilities  
- `pandas` & `openpyxl` - Data processing
- `sentence-transformers` - Semantic analysis (⭐ NEW!)
- `torch` - PyTorch for transformers
- `flask` - Web framework

**Note**: First run will download ~400MB of pre-trained models.

### Step 4: Start the Web Application

```bash
python3 web_app.py
```

**Expected Output:**
```
Loading semantic model: all-MiniLM-L6-v2...
Semantic model loaded successfully!
✅ Semantic analysis enabled (NLP-based)
🚀 Starting Student Introduction Evaluation Web App...
📱 Open in Chrome: http://localhost:5000
* Running on http://127.0.0.1:5000
```

### Step 5: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### Step 6: Test the Application

1. Click **"📋 Load Sample"** button
2. Click **"🚀 Evaluate"** button
3. View results!

---

## ☁️ Cloud Deployment Options

### Option 1: Heroku (Free Tier)

#### 1.1 Setup Files

Create `Procfile`:
```
web: gunicorn web_app:app
```

Create `runtime.txt`:
```
python-3.11.0
```

Add to `requirements.txt`:
```
gunicorn>=21.0.0
```

#### 1.2 Deploy

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create student-intro-evaluator

# Deploy
git push heroku main

# Open app
heroku open
```

**Note**: Heroku free tier may timeout on first request due to model loading.

---

### Option 2: Railway.app (Recommended)

#### 2.1 Setup

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Select your repository

#### 2.2 Configuration

Add environment variable:
```
PYTHON_VERSION=3.11
```

Railway auto-detects Flask and deploys!

**Advantages:**
- Fast deployment
- Free 500 hours/month
- No cold starts
- Good for ML models

---

### Option 3: Render (Free)

#### 3.1 Create `render.yaml`

```yaml
services:
  - type: web
    name: student-evaluator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn web_app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### 3.2 Deploy

1. Go to [render.com](https://render.com)
2. New Web Service
3. Connect GitHub repository
4. Render auto-deploys!

---

### Option 4: AWS EC2 (Free Tier)

#### 4.1 Launch EC2 Instance

```bash
# Launch t2.micro (free tier)
# OS: Ubuntu 22.04 LTS
```

#### 4.2 SSH and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/student-introduction-evaluator.git
cd student-introduction-evaluator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 web_app:app
```

#### 4.3 Keep Running (with systemd)

Create `/etc/systemd/system/evaluator.service`:

```ini
[Unit]
Description=Student Evaluator Web App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/student-introduction-evaluator
Environment="PATH=/home/ubuntu/student-introduction-evaluator/venv/bin"
ExecStart=/home/ubuntu/student-introduction-evaluator/venv/bin/gunicorn --bind 0.0.0.0:5000 web_app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable evaluator
sudo systemctl start evaluator
sudo systemctl status evaluator
```

---

### Option 5: DigitalOcean App Platform

#### 5.1 Setup

1. Push code to GitHub
2. Go to [DigitalOcean](https://www.digitalocean.com)
3. Create App → GitHub → Select repo
4. App Platform auto-detects Python!

#### 5.2 Configuration

- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn web_app:app`
- **HTTP Port**: 8080 (auto-configured)

**Cost**: $5/month (cheapest option)

---

## 🔧 Production Optimizations

### 1. Use Production WSGI Server

Replace development server with Gunicorn:

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 web_app:app
```

### 2. Add Nginx Reverse Proxy (Optional)

Install Nginx:
```bash
sudo apt install nginx
```

Configure `/etc/nginx/sites-available/evaluator`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Enable HTTPS (Optional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 4. Optimize Model Loading

Cache models to reduce startup time:

```python
# In web_app.py
from functools import lru_cache

@lru_cache(maxsize=1)
def get_evaluator():
    return StudentEvaluator(use_semantic=True)

# Use in routes
evaluator = get_evaluator()
```

---

## 🐳 Docker Deployment (Advanced)

### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "web_app:app"]
```

### Build and Run

```bash
# Build image
docker build -t student-evaluator .

# Run container
docker run -p 5000:5000 student-evaluator
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

Run:
```bash
docker-compose up -d
```

---

## 📱 Mobile Access

### Make accessible on local network:

```bash
# Find your IP
ifconfig  # macOS/Linux
ipconfig  # Windows

# Run server on all interfaces  
python3 web_app.py
# Server runs on 0.0.0.0:5000

# Access from mobile
http://YOUR_IP_ADDRESS:5000
```

---

## 🔍 Troubleshooting

### Issue 1: Port Already in Use

```bash
# Kill process on port 5000
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue 2: Model Download Fails

```bash
# Manually download models
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Issue 3: Out of Memory

```python
# Disable semantic analysis
evaluator = StudentEvaluator(use_semantic=False)
```

### Issue 4: Java Not Found (LanguageTool)

LanguageTool will auto-fallback. To install Java:

**macOS:**
```bash
brew install openjdk
```

**Ubuntu:**
```bash
sudo apt install default-jre
```

---

## 📊 Performance Tips

### 1. Reduce Model Size

Use smaller transformer model:
```python
semantic_analyzer = SemanticAnalyzer(model_name='paraphrase-MiniLM-L3-v2')
```

### 2. Enable Caching

Add Redis for caching results:

```bash
pip install redis
```

### 3. Load Balancing

Use multiple Gunicorn workers:
```bash
gunicorn --workers 4 --threads 2 web_app:app
```

---

## ✅ Deployment Checklist

- [ ] Requirements.txt up to date
- [ ] Virtual environment created
- [ ] Dependencies installed successfully
- [ ] Models downloaded (~400MB)
- [ ] Application starts without errors
- [ ] Web interface loads portsorrectly
- [ ] Sample evaluation works (85/100 score)
- [ ] Semantic analysis enabled
- [ ] Production server configured (Gunicorn)
- [ ] GitHub repository created
- [ ] README.md updated
- [ ] Deployment platform selected
- [ ] Environment variables set (if needed)
- [ ] Application deployed and accessible
- [ ] Screen recording created

---

## 🎥 Creating Screen Recording

### macOS (QuickTime)

1. Open QuickTime Player
2. File → New Screen Recording
3. Record the demo
4. Save as MP4

### Windows (Built-in)

1. Press `Win + G`
2. Click Record button
3. Demo the app
4. Save recording

### Loom (Cross-platform)

1. Install Loom extension
2. Record screen + webcam
3. Share link

---

## 📧 Support

For issues or questions:
- GitHub Issues: [repository-url]/issues
- Email: your-email@example.com

---

**Last Updated**: 2025-11-23  
**Version**: 2.0 (with semantic analysis)
