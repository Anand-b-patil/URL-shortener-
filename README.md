# 🔗 Smart URL Shortener with Analytics

A production-ready, full-stack URL shortener application with powerful analytics, built with Flask and modern web technologies.

![URL Shortener](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Core Features
- ✅ **URL Shortening**: Convert long URLs into short, memorable links
- ✅ **Custom Short Codes**: Create personalized short URLs
- ✅ **Click Tracking**: Track clicks and engagement for each link
- ✅ **Analytics Dashboard**: Beautiful dashboard with charts and statistics
- ✅ **QR Code Generation**: Auto-generate QR codes for every short URL
- ✅ **Link Expiry**: Set expiration dates for time-sensitive links
- ✅ **URL Validation**: Robust URL validation before shortening
- ✅ **Collision Prevention**: Unique short code generation with collision checking

### Technical Features
- 🚀 **RESTful API**: Complete REST API for integrations
- 📊 **Real-time Analytics**: Track clicks, creation dates, and more
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS
- 🔒 **Secure**: Input validation and error handling
- 📱 **Mobile Responsive**: Works perfectly on all devices
- ⚡ **Fast & Efficient**: Optimized database queries
- 🎯 **Production Ready**: Includes deployment configurations

---

## 📁 Project Structure

```
url-shortener/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration (Render)
├── runtime.txt                 # Python version specification
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── setup.bat                   # Windows setup script
├── README.md                   # This file
│
├── templates/                  # HTML templates (place template files here)
│   ├── index.html             # Home page
│   ├── dashboard.html         # Analytics dashboard
│   ├── 404.html               # Not found page
│   ├── expired.html           # Expired link page
│   └── 500.html               # Server error page
│
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
│
└── instance/                   # Instance-specific files
    └── urls.db                 # SQLite database (auto-generated)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (recommended: Python 3.11)
- pip (Python package manager)
- Git (optional)

### Installation Steps

#### 1. Clone or Download the Project

```bash
# Option 1: Clone with Git
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener

# Option 2: Download and extract the ZIP file
```

#### 2. Set Up the Project (Windows)

**Easy Method - Run Setup Script:**
```cmd
setup.bat
```

**Manual Method:**

```bash
# Create templates and static directories
mkdir templates
mkdir static

# Copy template files to templates folder
# Move *_template.html files to templates/ and rename them:
# - index_template.html → templates/index.html
# - dashboard_template.html → templates/dashboard.html
# - 404_template.html → templates/404.html
# - expired_template.html → templates/expired.html
# - 500_template.html → templates/500.html

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment Variables (Optional)

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and set your SECRET_KEY
# For production, use a strong random key
```

#### 4. Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## 📖 Usage Guide

### Creating a Short URL

1. Open your browser and go to `http://localhost:5000`
2. Enter your long URL in the input field
3. (Optional) Enter a custom short code (3-20 characters)
4. (Optional) Select an expiry period for the link
5. Click "Shorten URL"
6. Copy your short URL and QR code!

### Viewing Analytics

1. Click "Dashboard" in the navigation
2. View comprehensive statistics:
   - Total URLs created
   - Total clicks across all URLs
   - Number of custom URLs
   - Average clicks per URL
3. See charts showing:
   - Top 5 most clicked URLs
   - URL creation timeline
4. Browse the complete table of all URLs with:
   - Click counts
   - Creation dates
   - Actions (copy, delete)

### API Endpoints

#### 1. Shorten URL
```http
POST /api/shorten
Content-Type: application/json

{
    "url": "https://example.com/very-long-url",
    "custom_code": "mylink",          // Optional
    "expires_in_days": 30              // Optional
}

Response:
{
    "id": 1,
    "original_url": "https://example.com/very-long-url",
    "short_code": "mylink",
    "short_url": "http://localhost:5000/mylink",
    "clicks": 0,
    "created_at": "2024-03-20 10:30:00",
    "expires_at": "2024-04-20 10:30:00",
    "custom": true,
    "qr_code": "data:image/png;base64,..."
}
```

#### 2. Get All URLs (with pagination)
```http
GET /api/stats?page=1&per_page=10&sort_by=clicks&order=desc

Response:
{
    "urls": [...],
    "total": 50,
    "pages": 5,
    "current_page": 1,
    "per_page": 10
}
```

#### 3. Get Specific URL Stats
```http
GET /api/stats/mylink

Response:
{
    "id": 1,
    "original_url": "https://example.com/very-long-url",
    "short_code": "mylink",
    "clicks": 42,
    ...
}
```

#### 4. Delete URL
```http
DELETE /api/delete/mylink

Response:
{
    "message": "URL deleted successfully"
}
```

#### 5. Redirect (automatically increments clicks)
```http
GET /mylink

Response: 302 Redirect to original URL
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    custom_code BOOLEAN DEFAULT FALSE,
    clicks INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NULL
);

CREATE INDEX idx_short_code ON urls(short_code);
```

---

## 🌐 Deployment

### Deploy to Render (Recommended)

1. **Create a Render Account**: Sign up at [render.com](https://render.com)

2. **Connect Your Repository**:
   - Push your code to GitHub
   - Connect your GitHub account to Render

3. **Create a New Web Service**:
   - Select your repository
   - Choose "Web Service"
   - Configure:
     - **Name**: your-url-shortener
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

4. **Set Environment Variables**:
   ```
   SECRET_KEY=your-production-secret-key-here
   FLASK_ENV=production
   ```

5. **Deploy**: Click "Create Web Service"

Your app will be live at: `https://your-url-shortener.onrender.com`

### Deploy to Railway

1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)

2. **New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**:
   - Railway auto-detects Python
   - Add environment variables:
     ```
     SECRET_KEY=your-secret-key
     ```

4. **Deploy**: Railway automatically deploys

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-url-shortener

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy to PythonAnywhere

1. Upload your files to PythonAnywhere
2. Create a new web app (Flask)
3. Configure WSGI file:
```python
import sys
path = '/home/yourusername/url-shortener'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```
4. Reload web app

---

## 🧪 Testing

### Test the Application Locally

```bash
# Test URL shortening
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://google.com"}'

# Test URL redirect
curl -L http://localhost:5000/[short_code]

# Test statistics
curl http://localhost:5000/api/stats
```

### Browser Testing Checklist

- [ ] Create a short URL with a long URL
- [ ] Create a custom short URL
- [ ] Set link expiry and verify
- [ ] Click the short URL and verify redirect
- [ ] Check click counter increments
- [ ] View dashboard and verify statistics
- [ ] Test QR code generation
- [ ] Copy short URL to clipboard
- [ ] Delete a URL
- [ ] Test responsive design on mobile

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_ENV=development  # or 'production'

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///urls.db

# Server
HOST=0.0.0.0
PORT=5000
```

### Customization

#### Change the Short Code Length
In `app.py`, modify the `generate_short_code` function:
```python
def generate_short_code(length=8):  # Change from 6 to 8
    ...
```

#### Change Database
Replace SQLite with PostgreSQL:
```python
# In app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

#### Add Rate Limiting
Install Flask-Limiter:
```bash
pip install Flask-Limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@limiter.limit("10 per minute")
@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    ...
```

---

## 📊 Features Explained

### 1. **URL Validation**
- Checks URL format using regex
- Validates protocol (http/https)
- Normalizes URLs (adds http:// if missing)

### 2. **Short Code Generation**
- Random alphanumeric codes (6 characters by default)
- Collision detection and prevention
- Custom code validation (3-20 characters)

### 3. **Click Tracking**
- Automatic click counter increment
- No duplicate counting per session
- Real-time statistics

### 4. **QR Code Generation**
- Auto-generated for every short URL
- PNG format, base64 encoded
- Downloadable from the UI

### 5. **Link Expiry**
- Set expiration dates (1 day to 1 year)
- Automatic expiry checking on redirect
- Custom expiry page (410 error)

### 6. **Analytics Dashboard**
- Real-time statistics
- Interactive charts (Chart.js)
- Sortable and paginated table
- Export-ready data

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: `sqlite3.OperationalError: no such table: urls`
```bash
# Solution: Initialize database
python
>>> from app import db, app
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

**Issue**: Templates not found
```bash
# Solution: Ensure templates directory exists and contains HTML files
# Check that files are named correctly (without _template suffix)
```

**Issue**: Port 5000 already in use
```bash
# Solution: Change port in app.py or kill the process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port:
app.run(debug=True, port=5001)
```

**Issue**: QR code not generating
```bash
# Solution: Reinstall Pillow
pip uninstall Pillow
pip install Pillow
```

---

## 🎨 Screenshots

### Home Page
Beautiful gradient design with URL shortening form, custom code input, and expiry options.

### Dashboard
Comprehensive analytics with:
- Statistics cards (Total URLs, Clicks, Custom URLs, Average)
- Top 5 URLs bar chart
- Timeline line chart
- Complete URLs table with actions

### QR Code Display
Auto-generated QR codes for easy sharing on print materials and mobile devices.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See below:

```
MIT License

Copyright (c) 2024 Smart URL Shortener

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- Flask - The web framework
- Tailwind CSS - For beautiful styling
- Chart.js - For analytics charts
- QRCode - For QR code generation
- Font Awesome - For icons

---

## 📞 Support

If you have questions or need help:

- 📧 Open an issue on GitHub
- 💬 Check existing issues and discussions
- 📚 Read the documentation above

---

## 🚀 What's Next?

Planned features for future releases:

- [ ] User authentication and personal dashboards
- [ ] Bulk URL shortening
- [ ] API key management
- [ ] Advanced analytics (geolocation, devices, browsers)
- [ ] Link editing capabilities
- [ ] Password-protected links
- [ ] Domain customization
- [ ] Export analytics to CSV/PDF
- [ ] Webhook notifications
- [ ] Browser extension

---

## ⭐ Star This Project

If you find this project helpful, please give it a star on GitHub! It helps others discover this project.

---

**Built with ❤️ using Flask, Python, and modern web technologies**

**Happy URL Shortening! 🔗✨**
#   U R L - s h o r t e n e r - 
 
 