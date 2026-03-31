# 🔗 Smart URL Shortener with Advanced Analytics

A **production-ready full-stack URL shortener** built using Flask, featuring real-time analytics, QR code generation, and scalable architecture.

---

## 🚀 Live Demo

👉 https://url-shortener-qa38.onrender.com/

---

## ✨ Features

### 🔹 Core Features

* Shorten long URLs into clean, shareable links
* Custom short codes (user-defined aliases)
* Automatic QR code generation
* Link expiration (time-based)
* URL validation and sanitization

### 🔹 Analytics & Insights

* Real-time click tracking
* Dashboard with statistics:

  * Total URLs
  * Total clicks
  * Top performing links
* Interactive charts using Chart.js

### 🔹 Technical Highlights

* RESTful API architecture
* Collision-resistant short code generation
* Secure input handling
* Mobile-responsive UI (Tailwind CSS)
* Optimized database queries

---

## 🏗️ Tech Stack

### Frontend

* HTML5
* Tailwind CSS
* JavaScript
* Chart.js

### Backend

* Python (Flask)
* REST APIs

### Database

* SQLite (Development)
* PostgreSQL (Production-ready)

---

## 📁 Project Structure

```
url-shortener/
│
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── 404.html
│   ├── expired.html
│   └── 500.html
│
├── static/
│   ├── css/
│   └── js/
│
└── instance/
    └── urls.db
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
cp .env.example .env
```

Update `.env`:

```env
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

### 4. Run Application

```bash
python app.py
```

👉 Open: `http://localhost:5000`

---

## 📖 Usage

### 🔗 Create Short URL

* Enter long URL
* Optional: custom code + expiry
* Click “Shorten”

### 📊 View Analytics

* Open Dashboard
* Monitor clicks and trends

### 🔁 Redirect

* Access short URL → auto redirect + click tracked

---

## 🔌 API Endpoints

### Create Short URL

```http
POST /api/shorten
```

### Get All URLs

```http
GET /api/stats
```

### Get Single URL Stats

```http
GET /api/stats/<short_code>
```

### Delete URL

```http
DELETE /api/delete/<short_code>
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
```

---

## 🌐 Deployment

### 🚀 Deploy on Render

```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Environment Variables

```
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

---

## 🔧 Future Enhancements

* 🔐 User authentication (login/signup)
* 🌍 Geo-location analytics
* 📱 Device & browser tracking
* ⚡ Redis caching for performance
* 📦 Bulk URL shortening
* 🔑 API key management
* 🔒 Password-protected links

---

## 🧪 Testing

```bash
# Shorten URL
curl -X POST http://localhost:5000/api/shorten \
-H "Content-Type: application/json" \
-d '{"url":"https://example.com"}'

# Redirect
curl -L http://localhost:5000/<short_code>
```

---

## 🧑‍💻 Author

**Anand**
Final Year CSE | ML & Full-Stack Enthusiast

---

## 📄 License

MIT License

---

## ⭐ Why This Project Stands Out

* Full-stack implementation (Frontend + Backend + DB)
* Real-world use case (URL management & analytics)
* Scalable architecture (API + deployment ready)
* Strong backend concepts (REST, DB design, validation)

---

## ❤️ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🧑‍💻 Contribute


