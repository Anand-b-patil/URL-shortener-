# PostgreSQL Migration Guide

This guide explains how to use PostgreSQL for production deployment on Render while maintaining SQLite for local development.

## 🎯 What Changed

### 1. **Database Configuration (app.py)**
The app now automatically detects the environment:
- **Production (Render)**: Uses PostgreSQL via `DATABASE_URL` environment variable
- **Local Development**: Uses SQLite (`urls.db`)

### 2. **Dependencies (requirements.txt)**
Added `psycopg2-binary==2.9.9` - PostgreSQL adapter for Python

### 3. **Connection Pool Settings**
Added SQLAlchemy engine options for better PostgreSQL performance:
- `pool_pre_ping`: Verifies connections before use
- `pool_recycle`: Recycles connections every 5 minutes

### 4. **Error Handling**
Enhanced database initialization with proper error handling and informative messages

---

## 🚀 Local Development Setup

### Step 1: Update Dependencies
```bash
# Activate your virtual environment first
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install new dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration
Create a `.env` file (copy from `.env.example`):
```bash
# Windows:
copy .env.example .env

# Linux/Mac:
cp .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=your-secret-key-change-this
FLASK_ENV=development
# Leave DATABASE_URL empty for SQLite
```

### Step 3: Test Locally with SQLite
```bash
python app.py
```

You should see:
```
🗄️  Using SQLite database (development mode)
✅ Database initialized successfully!
🚀 Starting Smart URL Shortener...
📍 Access the app at: http://localhost:5000
```

### Step 4: Test the Application
1. Open http://localhost:5000
2. Create a short URL
3. Test redirection
4. Check analytics dashboard

---

## 🐘 (Optional) Local PostgreSQL Testing

If you want to test PostgreSQL locally before deploying:

### Step 1: Install PostgreSQL
- **Windows**: Download from https://www.postgresql.org/download/windows/
- **Mac**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql`

### Step 2: Create a Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE url_shortener_dev;

# Exit
\q
```

### Step 3: Update .env
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/url_shortener_dev
```

### Step 4: Run the App
```bash
python app.py
```

You should see:
```
🗄️  Using PostgreSQL database
✅ Database initialized successfully!
```

---

## 🌐 Render Deployment

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Add PostgreSQL support for Render deployment"
git push origin main
```

### Step 2: Create PostgreSQL Database on Render

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `url-shortener-db` (or your choice)
   - **Database**: `url_shortener`
   - **User**: `url_shortener_user`
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 15 (or latest)
   - **Plan**: Free tier (or paid for production)
4. Click **"Create Database"**
5. Wait for deployment (takes 1-2 minutes)
6. **Copy the "Internal Database URL"** (starts with `postgresql://`)

### Step 3: Create Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `url-shortener-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free tier (or paid)

### Step 4: Configure Environment Variables

In the Render web service dashboard, go to **"Environment"** and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | *Paste the Internal Database URL from Step 2* |
| `SECRET_KEY` | *Generate a secure random string* |
| `PYTHON_VERSION` | `3.11.0` (or your preferred version) |

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Render will automatically:
   - Build your app
   - Install dependencies
   - Start gunicorn
   - Initialize the PostgreSQL database

### Step 6: Monitor Deployment
Watch the logs in Render dashboard. You should see:
```
🗄️  Using PostgreSQL database
✅ Database initialized successfully!
```

### Step 7: Test Your Deployed App
1. Click the URL provided by Render (e.g., `https://url-shortener-app.onrender.com`)
2. Test creating short URLs
3. Test redirection
4. Check analytics

---

## 🔍 Troubleshooting

### Issue: "Could not import psycopg2"
**Solution**: Make sure `psycopg2-binary` is in requirements.txt and reinstall:
```bash
pip install -r requirements.txt
```

### Issue: "Connection refused" on Render
**Solution**: Check environment variables:
- Ensure `DATABASE_URL` is set correctly
- Use **Internal Database URL** (not External)
- Verify the database is in "Available" status

### Issue: "FATAL: password authentication failed"
**Solution**: 
- Copy the DATABASE_URL exactly from Render database dashboard
- Don't modify the connection string
- Ensure no extra spaces

### Issue: "relation 'urls' does not exist"
**Solution**: Database tables weren't created. Check logs:
- Look for "✅ Database initialized successfully!"
- If missing, the app might have crashed before init_db()
- Check for Python syntax errors in logs

### Issue: Render service keeps restarting
**Solution**: Check logs for errors:
1. Go to Render dashboard → Your web service → Logs
2. Look for Python errors or database connection issues
3. Common causes:
   - Missing environment variables
   - Wrong DATABASE_URL format
   - Syntax errors in code

---

## 📊 Verify Database Migration

### Check PostgreSQL Connection
On Render, go to your web service logs and verify you see:
```
🗄️  Using PostgreSQL database
```

### Inspect Database (Optional)
Connect to your Render PostgreSQL database:

1. In Render dashboard, go to your PostgreSQL database
2. Copy the **"External Database URL"**
3. Use a database client (TablePlus, DBeaver, pgAdmin) or psql:

```bash
psql "postgresql://user:password@host:port/database"

# List tables
\dt

# Check URLs table structure
\d urls

# View data
SELECT * FROM urls LIMIT 10;
```

---

## 🔄 Rolling Back to SQLite (If Needed)

If you need to rollback:

1. Remove or comment out DATABASE_URL in .env
2. Restart the app
3. App will automatically use SQLite

---

## 📝 Important Notes

### Database URL Format
Render provides URLs in format `postgres://...`, but SQLAlchemy 1.4+ requires `postgresql://`. The code automatically handles this conversion:

```python
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
```

### Connection Pooling
PostgreSQL connection pooling is configured for optimal performance:
- `pool_pre_ping=True`: Tests connections before use (prevents stale connections)
- `pool_recycle=300`: Recycles connections every 5 minutes

### Data Persistence
- **SQLite**: Data stored in `instance/urls.db` file (local only)
- **PostgreSQL**: Data stored in Render's managed PostgreSQL service (persistent across deployments)

### Free Tier Limitations
Render free tier:
- PostgreSQL: 1GB storage, expires after 90 days of inactivity
- Web Service: Spins down after 15 minutes of inactivity (first request takes ~30 seconds)

---

## ✅ Success Checklist

- [ ] `psycopg2-binary` added to requirements.txt
- [ ] App runs locally with SQLite
- [ ] PostgreSQL database created on Render
- [ ] Web service deployed on Render
- [ ] DATABASE_URL environment variable set
- [ ] SECRET_KEY environment variable set
- [ ] App logs show "Using PostgreSQL database"
- [ ] Can create short URLs on deployed app
- [ ] Redirection works on deployed app
- [ ] Analytics dashboard shows data

---

## 🎉 You're Done!

Your Smart URL Shortener now uses:
- **SQLite** for local development (easy, no setup)
- **PostgreSQL** for production on Render (scalable, reliable)

The app automatically detects the environment and uses the appropriate database!
