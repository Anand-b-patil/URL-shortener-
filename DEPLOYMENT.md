# 🚀 Deployment Guide for Smart URL Shortener

This guide covers deploying your URL Shortener to various platforms.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All dependencies are listed in `requirements.txt`
- [ ] Database is properly configured
- [ ] Environment variables are set
- [ ] Secret keys are changed from defaults
- [ ] Application runs locally without errors
- [ ] Git repository is clean and committed

---

## 🌐 Deployment Options

### 1. Render (Recommended - Free Tier Available)

**Why Render?**
- Free tier available
- Auto-deploys from GitHub
- Built-in SSL certificates
- Easy database management

**Steps:**

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/url-shortener.git
   git push -u origin main
   ```

2. **Sign Up & Connect:**
   - Go to [render.com](https://render.com)
   - Sign up and connect your GitHub account

3. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Select your repository
   - Configure:
     ```
     Name: url-shortener
     Environment: Python 3
     Region: Choose closest to you
     Branch: main
     Build Command: pip install -r requirements.txt
     Start Command: gunicorn app:app
     Instance Type: Free
     ```

4. **Add Environment Variables:**
   - Click "Environment"
   - Add variables:
     ```
     SECRET_KEY = your-random-secret-key-here
     PYTHON_VERSION = 3.11.0
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

**Using PostgreSQL on Render:**
```bash
# Add to requirements.txt:
psycopg2-binary==2.9.9

# Create PostgreSQL database in Render
# Copy Internal Database URL
# Add environment variable:
DATABASE_URL = postgresql://...
```

---

### 2. Railway (Easy & Fast)

**Why Railway?**
- Extremely simple deployment
- Automatic SSL
- $5 free credit monthly
- One-click deploys

**Steps:**

1. **Push to GitHub** (same as above)

2. **Deploy:**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure:**
   - Railway auto-detects Python
   - Add environment variable:
     ```
     SECRET_KEY = your-secret-key
     ```

4. **Generate Domain:**
   - Go to Settings → Generate Domain
   - Your app is live!

---

### 3. Heroku

**Why Heroku?**
- Well-established platform
- Great documentation
- Many add-ons available

**Steps:**

1. **Install Heroku CLI:**
   ```bash
   # Download from heroku.com/cli
   ```

2. **Login & Create App:**
   ```bash
   heroku login
   heroku create your-url-shortener
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open App:**
   ```bash
   heroku open
   ```

**Add PostgreSQL:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
# Database URL is auto-configured
```

---

### 4. PythonAnywhere (Free Tier Available)

**Why PythonAnywhere?**
- Free tier with no credit card required
- Simple Python hosting
- Good for beginners

**Steps:**

1. **Sign Up:**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Create free account

2. **Upload Files:**
   - Use "Files" tab to upload your project
   - Or clone from GitHub:
     ```bash
     cd ~
     git clone https://github.com/yourusername/url-shortener.git
     ```

3. **Install Dependencies:**
   - Open Bash console:
     ```bash
     cd ~/url-shortener
     pip3 install --user -r requirements.txt
     ```

4. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10

5. **Configure WSGI File:**
   - Click on WSGI configuration file
   - Replace contents with:
     ```python
     import sys
     import os
     
     # Add your project directory
     path = '/home/yourusername/url-shortener'
     if path not in sys.path:
         sys.path.append(path)
     
     # Set environment variables
     os.environ['SECRET_KEY'] = 'your-secret-key'
     
     from app import app as application
     ```

6. **Reload Web App:**
   - Click "Reload" button
   - Visit `yourusername.pythonanywhere.com`

---

### 5. Google Cloud Platform (GCP)

**Using Google App Engine:**

1. **Create `app.yaml`:**
   ```yaml
   runtime: python311
   
   env_variables:
     SECRET_KEY: 'your-secret-key'
   
   handlers:
   - url: /static
     static_dir: static
   
   - url: /.*
     script: auto
   ```

2. **Deploy:**
   ```bash
   gcloud app deploy
   ```

---

### 6. AWS Elastic Beanstalk

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p python-3.11 url-shortener
   ```

3. **Create Environment:**
   ```bash
   eb create url-shortener-env
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

---

### 7. DigitalOcean App Platform

1. **Push to GitHub**

2. **Create App:**
   - Go to [digitalocean.com](https://www.digitalocean.com)
   - Create → Apps
   - Connect GitHub repository

3. **Configure:**
   ```
   Build Command: pip install -r requirements.txt
   Run Command: gunicorn app:app
   ```

4. **Add Environment Variables:**
   ```
   SECRET_KEY = your-secret-key
   ```

5. **Deploy**

---

## 🔐 Production Configuration

### Environment Variables

Always set these in production:

```env
# Required
SECRET_KEY=generate-a-strong-random-key-here

# Optional
FLASK_ENV=production
DATABASE_URL=your-database-url
PORT=8080
```

### Generate Strong Secret Key:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Security Best Practices:

1. **Never commit secrets:**
   ```bash
   # Add to .gitignore:
   .env
   *.db
   ```

2. **Use HTTPS:**
   - Most platforms provide free SSL
   - Force HTTPS in production

3. **Set secure headers:**
   ```python
   # Add to app.py:
   from flask_talisman import Talisman
   if app.config['ENV'] == 'production':
       Talisman(app)
   ```

4. **Rate limiting:**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app)
   ```

---

## 📊 Database Options

### SQLite (Default - Development)
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///urls.db'
```

### PostgreSQL (Recommended - Production)
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@host:port/dbname'
```

### MySQL
```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@host:port/dbname'
```

---

## 🔍 Monitoring & Logging

### Add Logging:

```python
import logging

# In app.py:
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    logger.info(f"Shortening URL: {original_url}")
    # ... rest of code
```

### Error Tracking (Sentry):

```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

---

## 🧪 Testing Before Deployment

```bash
# Test with production settings
export FLASK_ENV=production
export SECRET_KEY=test-key

python app.py

# Run automated tests
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://google.com"}'
```

---

## 📈 Performance Optimization

### 1. Use Production WSGI Server

Always use gunicorn in production:
```bash
gunicorn app:app --workers 4 --bind 0.0.0.0:8000
```

### 2. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/stats')
@cache.cached(timeout=300)  # 5 minutes
def get_stats():
    # ... code
```

### 3. Database Connection Pooling

```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

---

## 🎯 Domain Configuration

### Custom Domain Setup:

1. **Buy Domain** (Namecheap, Google Domains, etc.)

2. **Configure DNS:**
   ```
   Type: A or CNAME
   Name: @ or www
   Value: Your deployment URL/IP
   ```

3. **SSL Certificate:**
   - Most platforms auto-provision SSL
   - Or use Let's Encrypt

4. **Update App Config:**
   ```python
   app.config['SERVER_NAME'] = 'yourdomain.com'
   ```

---

## 🛠️ Troubleshooting Deployment

### Common Issues:

**Error: Application failed to start**
```bash
# Check logs:
# Render: View logs in dashboard
# Heroku: heroku logs --tail
# Railway: Check build logs

# Common causes:
# - Missing dependencies in requirements.txt
# - Wrong Python version
# - Database connection issues
```

**Error: 502 Bad Gateway**
```bash
# Check:
# - App is running
# - Port configuration correct
# - Gunicorn workers started
```

**Error: Database connection failed**
```bash
# Verify:
# - DATABASE_URL environment variable
# - Database credentials
# - Network access allowed
```

---

## ✅ Post-Deployment Checklist

After deployment:

- [ ] App loads successfully
- [ ] Can create short URLs
- [ ] Redirects work correctly
- [ ] Dashboard displays data
- [ ] QR codes generate
- [ ] Custom domains configured (if applicable)
- [ ] SSL certificate active
- [ ] Environment variables set
- [ ] Database connected
- [ ] Monitoring enabled

---

## 🎉 You're Live!

Congratulations! Your URL Shortener is now deployed.

**Share your creation:**
- 📱 Test on mobile devices
- 🔗 Share with friends
- 💼 Add to your portfolio
- ⭐ Star the GitHub repo

---

## 📞 Support

Need help with deployment?
- Check platform documentation
- Open GitHub issue
- Join community forums

**Happy Deploying! 🚀**
