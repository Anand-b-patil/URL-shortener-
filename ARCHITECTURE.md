# 🏗️ Architecture & Design Document

## Smart URL Shortener - Technical Architecture

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT SIDE                         │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────┐  │
│  │  Browser │  │  Mobile  │  │   API Clients       │  │
│  │   (Web)  │  │  Device  │  │ (Python, JS, cURL)  │  │
│  └─────┬────┘  └─────┬────┘  └──────────┬──────────┘  │
│        │             │                   │              │
└────────┼─────────────┼───────────────────┼──────────────┘
         │             │                   │
         └─────────────┴───────────────────┘
                       │
                       ▼ HTTP/HTTPS
         ┌─────────────────────────────────┐
         │      FLASK APPLICATION          │
         │  ┌──────────────────────────┐   │
         │  │   Application Layer      │   │
         │  │  ┌────────┐  ┌────────┐  │   │
         │  │  │ Routes │  │  API   │  │   │
         │  │  └────┬───┘  └───┬────┘  │   │
         │  └───────┼──────────┼───────┘   │
         │          │          │            │
         │  ┌───────▼──────────▼───────┐   │
         │  │   Business Logic Layer   │   │
         │  │  ┌─────────────────────┐ │   │
         │  │  │ URL Shortening      │ │   │
         │  │  │ Validation          │ │   │
         │  │  │ QR Code Generation  │ │   │
         │  │  │ Analytics           │ │   │
         │  │  └──────────┬──────────┘ │   │
         │  └─────────────┼────────────┘   │
         │                │                 │
         │  ┌─────────────▼────────────┐   │
         │  │    Database Layer        │   │
         │  │  (SQLAlchemy ORM)        │   │
         │  └─────────────┬────────────┘   │
         └────────────────┼──────────────── │
                          │
                          ▼
         ┌────────────────────────────────┐
         │      SQLite DATABASE           │
         │  ┌──────────────────────────┐  │
         │  │   URLs Table             │  │
         │  │  - id (PK)               │  │
         │  │  - original_url          │  │
         │  │  - short_code (UNIQUE)   │  │
         │  │  - clicks                │  │
         │  │  - created_at            │  │
         │  │  - expires_at            │  │
         │  │  - custom_code (bool)    │  │
         │  └──────────────────────────┘  │
         └────────────────────────────────┘
```

---

## 🔄 Request Flow Diagrams

### URL Shortening Flow

```
User enters URL
     │
     ▼
┌────────────────┐
│  Validate URL  │ ──[Invalid]──> Return Error 400
└────┬───────────┘
     │ [Valid]
     ▼
┌────────────────┐
│ Custom Code?   │
└────┬───────────┘
     │
     ├──[Yes]──> Check if available ──[Taken]──> Return Error 409
     │                │
     │                └──[Available]──┐
     │                                │
     └──[No]──> Generate random code ─┤
                                      │
                                      ▼
                         ┌─────────────────────┐
                         │  Create URL Entry   │
                         │  - Save to database │
                         │  - Generate QR code │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Return Response    │
                         │  - Short URL        │
                         │  - QR Code (base64) │
                         │  - Statistics       │
                         └─────────────────────┘
```

### URL Redirect Flow

```
User clicks short URL
     │
     ▼
┌────────────────────┐
│ Extract short code │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Query database     │
└─────────┬──────────┘
          │
          ├──[Not Found]──> Display 404 Page
          │
          ├──[Expired]────> Display 410 Page
          │
          └──[Found]──┐
                      │
                      ▼
          ┌───────────────────┐
          │ Increment Clicks  │
          └──────────┬────────┘
                     │
                     ▼
          ┌───────────────────┐
          │ Redirect (302)    │
          │ to original URL   │
          └───────────────────┘
```

### Analytics Dashboard Flow

```
User opens dashboard
     │
     ▼
┌─────────────────────┐
│ Request statistics  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Query all URLs      │
│ with pagination     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Calculate stats:    │
│ - Total URLs        │
│ - Total clicks      │
│ - Custom URLs       │
│ - Average clicks    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Generate charts:    │
│ - Top 5 URLs        │
│ - Timeline          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Render dashboard    │
│ with visualizations │
└─────────────────────┘
```

---

## 🗃️ Database Schema

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

### Field Descriptions:

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Auto-incrementing primary key |
| original_url | TEXT | The long URL to redirect to |
| short_code | VARCHAR(10) | Unique short code (6-8 chars) |
| custom_code | BOOLEAN | Whether code was custom or random |
| clicks | INTEGER | Number of times URL was accessed |
| created_at | DATETIME | Timestamp of creation |
| expires_at | DATETIME | Optional expiration date |

### Indexes:
- **PRIMARY KEY** on `id` - Fast row lookups
- **UNIQUE INDEX** on `short_code` - Prevents duplicates
- **INDEX** on `short_code` - Fast redirect lookups

---

## 🔌 API Architecture

### REST API Endpoints

```
┌─────────────────────────────────────────────────────┐
│                    REST API                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  POST /api/shorten                                  │
│  ├─ Input: { url, custom_code?, expires_in_days? } │
│  └─ Output: { short_url, qr_code, statistics }     │
│                                                     │
│  GET /api/stats                                     │
│  ├─ Query: ?page=1&per_page=10&sort_by=clicks      │
│  └─ Output: { urls[], total, pages }               │
│                                                     │
│  GET /api/stats/<short_code>                        │
│  └─ Output: { url_details, clicks, dates }         │
│                                                     │
│  DELETE /api/delete/<short_code>                    │
│  └─ Output: { message: "deleted" }                 │
│                                                     │
│  GET /<short_code>                                  │
│  └─ Output: 302 Redirect                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 Frontend Architecture

### Component Structure

```
┌─────────────────────────────────────────────────┐
│               Frontend Layer                     │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │         index.html (Home Page)          │   │
│  │  ┌───────────────────────────────────┐  │   │
│  │  │  URL Shortener Form               │  │   │
│  │  │  ├─ URL Input                     │  │   │
│  │  │  ├─ Custom Code Input             │  │   │
│  │  │  ├─ Expiry Selector               │  │   │
│  │  │  └─ Submit Button                 │  │   │
│  │  └───────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────┐  │   │
│  │  │  Result Display                   │  │   │
│  │  │  ├─ Short URL                     │  │   │
│  │  │  ├─ QR Code                       │  │   │
│  │  │  ├─ Statistics Cards              │  │   │
│  │  │  └─ Action Buttons                │  │   │
│  │  └───────────────────────────────────┘  │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │      dashboard.html (Analytics)         │   │
│  │  ┌───────────────────────────────────┐  │   │
│  │  │  Statistics Overview              │  │   │
│  │  │  ├─ Total URLs Card               │  │   │
│  │  │  ├─ Total Clicks Card             │  │   │
│  │  │  ├─ Custom URLs Card              │  │   │
│  │  │  └─ Average Clicks Card           │  │   │
│  │  └───────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────┐  │   │
│  │  │  Charts Section                   │  │   │
│  │  │  ├─ Top 5 URLs Bar Chart          │  │   │
│  │  │  └─ Timeline Line Chart           │  │   │
│  │  └───────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────┐  │   │
│  │  │  URLs Table                       │  │   │
│  │  │  ├─ Sortable Columns              │  │   │
│  │  │  ├─ Pagination                    │  │   │
│  │  │  └─ Action Buttons                │  │   │
│  │  └───────────────────────────────────┘  │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### JavaScript Event Flow

```
Page Load
   │
   ▼
Initialize
   ├─> Load Chart.js
   ├─> Load Font Awesome
   └─> Attach event listeners
   
Form Submit
   │
   ▼
Validate Input
   │
   ├─[Invalid]─> Show error
   │
   └─[Valid]──> Send API request
                    │
                    ▼
                Process Response
                    │
                    ├─[Success]─> Display result
                    │             ├─> Show QR code
                    │             └─> Show statistics
                    │
                    └─[Error]───> Show error message
```

---

## 🔒 Security Architecture

### Input Validation

```
User Input
   │
   ▼
┌──────────────────┐
│ URL Validation   │
│ ├─ Protocol      │ (http/https)
│ ├─ Domain format │ (valid domain)
│ └─ Length check  │ (max length)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Custom Code      │
│ ├─ Length (3-20) │
│ ├─ Characters    │ (alphanumeric, -, _)
│ └─ Availability  │ (not taken)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Sanitization     │
│ ├─ Strip spaces  │
│ ├─ Normalize URL │
│ └─ Escape chars  │
└────────┬─────────┘
         │
         ▼
    Process Request
```

### Security Layers

1. **Input Layer**
   - URL validation (regex)
   - Custom code validation
   - Length restrictions
   - Character whitelisting

2. **Application Layer**
   - CORS protection
   - Error handling
   - Input sanitization
   - SQL injection prevention (ORM)

3. **Database Layer**
   - Unique constraints
   - Indexed lookups
   - Transaction safety

---

## 📊 Data Flow

### Create URL Data Flow

```
[Client] ──request──> [Flask Route] ──validate──> [Business Logic]
                                                         │
                                                         ▼
                                                   ┌──────────┐
                                                   │ Generate │
                                                   │   Code   │
                                                   └────┬─────┘
                                                        │
                                                        ▼
[Client] <──response── [Flask Route] <──return── [Database]
  (JSON)                                          (SQLAlchemy)
```

### Redirect Data Flow

```
[Browser] ──GET /code──> [Flask Route]
                              │
                              ▼
                         [Database]
                              │
                              ├─> Increment clicks
                              │
                              └─> Get original URL
                                      │
                                      ▼
[Browser] <──302 Redirect── [Flask Route]
(Original URL)
```

---

## 🚀 Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────┐
│  Developer Machine                  │
│  ├─ Python 3.11                     │
│  ├─ Flask Dev Server (port 5000)    │
│  ├─ SQLite Database (local file)    │
│  └─ Debug Mode: ON                  │
└─────────────────────────────────────┘
```

### Production Environment

```
┌────────────────────────────────────────┐
│  Cloud Platform (Render/Railway)       │
│  ┌────────────────────────────────────┐│
│  │  Gunicorn WSGI Server             ││
│  │  ├─ Workers: 4                    ││
│  │  ├─ Timeout: 30s                  ││
│  │  └─ Port: 8000                    ││
│  └────────────────────────────────────┘│
│  ┌────────────────────────────────────┐│
│  │  PostgreSQL Database (optional)    ││
│  │  ├─ Connection pooling            ││
│  │  └─ Automatic backups             ││
│  └────────────────────────────────────┘│
│  ┌────────────────────────────────────┐│
│  │  SSL/TLS Certificate              ││
│  │  (Automatic via platform)         ││
│  └────────────────────────────────────┘│
└────────────────────────────────────────┘
```

---

## 📈 Performance Considerations

### Database Optimization

```sql
-- Indexed queries (O(log n))
SELECT * FROM urls WHERE short_code = 'abc123';

-- Efficient pagination
SELECT * FROM urls 
ORDER BY created_at DESC 
LIMIT 10 OFFSET 0;

-- Click tracking (single update)
UPDATE urls 
SET clicks = clicks + 1 
WHERE short_code = 'abc123';
```

### Caching Strategy (Future)

```
┌────────────────┐
│   Client       │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Redis Cache   │ ←──── Hot URLs
└───────┬────────┘       (frequently accessed)
        │
        └─[Miss]──> Database
```

---

## 🧩 Technology Stack Details

```
┌─────────────────────────────────────────┐
│          Technology Stack               │
├─────────────────────────────────────────┤
│                                         │
│  Backend                                │
│  ├─ Framework: Flask 3.0                │
│  ├─ ORM: SQLAlchemy 3.1                 │
│  ├─ Database: SQLite (dev)              │
│  ├─ Server: Gunicorn (prod)             │
│  └─ Language: Python 3.11               │
│                                         │
│  Frontend                               │
│  ├─ HTML5                               │
│  ├─ CSS: Tailwind CSS 2.2               │
│  ├─ JavaScript: Vanilla ES6+            │
│  ├─ Charts: Chart.js 4.4                │
│  └─ Icons: Font Awesome 6.4             │
│                                         │
│  Libraries                              │
│  ├─ QR Codes: qrcode 7.4                │
│  ├─ Images: Pillow 10.1                 │
│  └─ CORS: Flask-CORS 4.0                │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔄 State Management

### Application States

```
┌──────────────┐
│   Idle       │
└──────┬───────┘
       │
       ├──[Create URL]──> Loading ──> Success/Error
       │
       ├──[Redirect]────> Query ────> Redirect/404
       │
       └──[Dashboard]───> Loading ──> Display Stats
```

### Database Transactions

```python
# Atomic operations
try:
    url = URL(original_url=url, short_code=code)
    db.session.add(url)
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    # Handle duplicate
```

---

## 📝 Design Patterns Used

### 1. MVC Pattern
- **Model:** SQLAlchemy models (URLs table)
- **View:** Jinja2 templates (HTML)
- **Controller:** Flask routes (business logic)

### 2. Repository Pattern
- Database abstraction through SQLAlchemy ORM

### 3. Factory Pattern
- Flask app creation and configuration

### 4. Singleton Pattern
- Database session management

---

## 🎯 Future Architecture Enhancements

```
Current:
[Client] ──> [Flask] ──> [SQLite]

Future:
                ┌──> [Redis Cache]
                │
[Client] ──> [Load Balancer] ──> [Flask×N] ──> [PostgreSQL]
                │                      │
                │                      └──> [Analytics DB]
                │
                └──> [CDN] (for static files)
```

---

**This architecture supports:**
- ✅ Easy scaling
- ✅ High availability
- ✅ Fast response times
- ✅ Secure operations
- ✅ Simple maintenance

---

