"""
Smart URL Shortener with Analytics - Main Flask Application
Production-ready URL shortener with complete analytics and REST API
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import string
import random
import re
import os
import qrcode
import io
import base64
from urllib.parse import urlparse

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration with PostgreSQL support
# Use DATABASE_URL from environment (Render provides this automatically)
# Falls back to SQLite for local development
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Render PostgreSQL URL fix: postgres:// -> postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"🗄️  Using PostgreSQL database")
else:
    # Local development - use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
    print(f"🗄️  Using SQLite database (development mode)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Verify connections before using them
    'pool_recycle': 300,    # Recycle connections after 5 minutes
}

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# ============================================
# DATABASE MODELS
# ============================================

class URL(db.Model):
    """URL model for storing shortened URLs with analytics"""
    __tablename__ = 'urls'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    custom_code = db.Column(db.Boolean, default=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<URL {self.short_code}>'
    
    def to_dict(self):
        """Convert URL object to dictionary for JSON response"""
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'short_url': request.host_url + self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M:%S') if self.expires_at else None,
            'custom': self.custom_code
        }

# ============================================
# UTILITY FUNCTIONS
# ============================================

def validate_url(url):
    """Validate URL format using regex"""
    regex = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def normalize_url(url):
    """Normalize URL by adding http:// if missing"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def generate_short_code(length=6):
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_unique_short_code(custom_code=None, max_attempts=10):
    """Generate a unique short code with collision checking"""
    if custom_code:
        # Check if custom code is available
        if URL.query.filter_by(short_code=custom_code).first():
            return None
        return custom_code
    
    # Generate random code with collision checking
    for _ in range(max_attempts):
        code = generate_short_code()
        if not URL.query.filter_by(short_code=code).first():
            return code
    
    # If still colliding, increase length
    return generate_short_code(length=8)

def generate_qr_code(url):
    """Generate QR code for URL and return base64 encoded image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"

# ============================================
# ROUTES - WEB PAGES
# ============================================

@app.route('/')
def index():
    """Home page with URL shortener form"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard page"""
    return render_template('dashboard.html')

# ============================================
# API ROUTES
# ============================================

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    API endpoint to shorten a URL
    Expected JSON: {"url": "long_url", "custom_code": "optional", "expires_in_days": optional}
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url'].strip()
        custom_code = data.get('custom_code', '').strip()
        expires_in_days = data.get('expires_in_days')
        
        # Normalize URL
        original_url = normalize_url(original_url)
        
        # Validate URL
        if not validate_url(original_url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Check if URL already exists
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url and not custom_code:
            # Return existing short URL
            response_data = existing_url.to_dict()
            response_data['qr_code'] = generate_qr_code(response_data['short_url'])
            return jsonify(response_data), 200
        
        # Validate custom code if provided
        if custom_code:
            if len(custom_code) < 3 or len(custom_code) > 20:
                return jsonify({'error': 'Custom code must be between 3 and 20 characters'}), 400
            
            if not re.match(r'^[a-zA-Z0-9_-]+$', custom_code):
                return jsonify({'error': 'Custom code can only contain letters, numbers, hyphens, and underscores'}), 400
        
        # Generate unique short code
        short_code = get_unique_short_code(custom_code)
        
        if not short_code:
            return jsonify({'error': 'Custom code already taken. Please choose another.'}), 409
        
        # Calculate expiry date
        expires_at = None
        if expires_in_days:
            try:
                days = int(expires_in_days)
                if days > 0:
                    expires_at = datetime.utcnow() + timedelta(days=days)
            except ValueError:
                pass
        
        # Create new URL entry
        new_url = URL(
            original_url=original_url,
            short_code=short_code,
            custom_code=bool(custom_code),
            expires_at=expires_at
        )
        
        db.session.add(new_url)
        db.session.commit()
        
        # Prepare response
        response_data = new_url.to_dict()
        response_data['qr_code'] = generate_qr_code(response_data['short_url'])
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get all URLs with analytics data
    Supports pagination and sorting
    """
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')
        
        # Query with sorting
        query = URL.query
        
        if sort_by == 'clicks':
            query = query.order_by(URL.clicks.desc() if order == 'desc' else URL.clicks.asc())
        elif sort_by == 'created_at':
            query = query.order_by(URL.created_at.desc() if order == 'desc' else URL.created_at.asc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        urls = [url.to_dict() for url in pagination.items]
        
        return jsonify({
            'urls': urls,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_url_stats(short_code):
    """Get statistics for a specific short URL"""
    try:
        url = URL.query.filter_by(short_code=short_code).first()
        
        if not url:
            return jsonify({'error': 'Short URL not found'}), 404
        
        return jsonify(url.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/delete/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    """Delete a short URL"""
    try:
        url = URL.query.filter_by(short_code=short_code).first()
        
        if not url:
            return jsonify({'error': 'Short URL not found'}), 404
        
        db.session.delete(url)
        db.session.commit()
        
        return jsonify({'message': 'URL deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# ============================================
# URL REDIRECTION
# ============================================

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect short URL to original URL and increment click counter"""
    try:
        url = URL.query.filter_by(short_code=short_code).first()
        
        if not url:
            return render_template('404.html', short_code=short_code), 404
        
        # Check if URL has expired
        if url.expires_at and datetime.utcnow() > url.expires_at:
            return render_template('expired.html', short_code=short_code), 410
        
        # Increment click counter
        url.clicks += 1
        db.session.commit()
        
        # Redirect to original URL
        return redirect(url.original_url)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():
    """Initialize database with error handling"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        print("⚠️  Please check your database connection settings")
        raise

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    # Import timedelta for expiry feature
    from datetime import timedelta
    
    # Initialize database
    init_db()
    
    # Run the app
    print("🚀 Starting Smart URL Shortener...")
    print("📍 Access the app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
