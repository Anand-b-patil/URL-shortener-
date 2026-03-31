# 📚 API Documentation - Smart URL Shortener

Complete REST API documentation for the Smart URL Shortener application.

**Base URL:** `http://localhost:5000` (development) or `https://your-domain.com` (production)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Endpoints Overview](#endpoints-overview)
3. [API Reference](#api-reference)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## 🔐 Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

**Future Enhancement:** API key authentication will be added in a future version.

---

## 📍 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shorten` | Create a shortened URL |
| GET | `/api/stats` | Get all URLs with pagination |
| GET | `/api/stats/<short_code>` | Get specific URL statistics |
| DELETE | `/api/delete/<short_code>` | Delete a shortened URL |
| GET | `/<short_code>` | Redirect to original URL |

---

## 🔧 API Reference

### 1. Create Short URL

Create a new shortened URL with optional custom code and expiry.

**Endpoint:** `POST /api/shorten`

**Headers:**
```http
Content-Type: application/json
```

**Request Body:**
```json
{
    "url": "https://example.com/very-long-url",  // Required
    "custom_code": "mylink",                      // Optional
    "expires_in_days": 30                         // Optional
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | The long URL to shorten. Must be a valid HTTP/HTTPS URL |
| custom_code | string | No | Custom short code (3-20 characters, alphanumeric, hyphens, underscores) |
| expires_in_days | integer | No | Number of days until the link expires (1-365) |

**Success Response (201 Created):**
```json
{
    "id": 1,
    "original_url": "https://example.com/very-long-url",
    "short_code": "mylink",
    "short_url": "http://localhost:5000/mylink",
    "clicks": 0,
    "created_at": "2024-03-20 10:30:00",
    "expires_at": "2024-04-20 10:30:00",
    "custom": true,
    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Error Responses:**

```json
// 400 Bad Request - Missing URL
{
    "error": "URL is required"
}

// 400 Bad Request - Invalid URL
{
    "error": "Invalid URL format"
}

// 400 Bad Request - Invalid custom code
{
    "error": "Custom code must be between 3 and 20 characters"
}

// 409 Conflict - Custom code taken
{
    "error": "Custom code already taken. Please choose another."
}

// 500 Internal Server Error
{
    "error": "Server error: [error details]"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.google.com",
    "custom_code": "google",
    "expires_in_days": 30
  }'
```

**JavaScript Example:**
```javascript
fetch('http://localhost:5000/api/shorten', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        url: 'https://www.google.com',
        custom_code: 'google',
        expires_in_days: 30
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/shorten"
payload = {
    "url": "https://www.google.com",
    "custom_code": "google",
    "expires_in_days": 30
}

response = requests.post(url, json=payload)
print(response.json())
```

---

### 2. Get All URLs (with Pagination)

Retrieve all shortened URLs with pagination and sorting options.

**Endpoint:** `GET /api/stats`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| per_page | integer | 10 | Items per page (max: 100) |
| sort_by | string | created_at | Sort field: 'created_at' or 'clicks' |
| order | string | desc | Sort order: 'asc' or 'desc' |

**Success Response (200 OK):**
```json
{
    "urls": [
        {
            "id": 1,
            "original_url": "https://example.com/long-url",
            "short_code": "abc123",
            "short_url": "http://localhost:5000/abc123",
            "clicks": 42,
            "created_at": "2024-03-20 10:30:00",
            "expires_at": null,
            "custom": false
        },
        // ... more URLs
    ],
    "total": 50,
    "pages": 5,
    "current_page": 1,
    "per_page": 10
}
```

**cURL Example:**
```bash
curl "http://localhost:5000/api/stats?page=1&per_page=20&sort_by=clicks&order=desc"
```

**JavaScript Example:**
```javascript
fetch('http://localhost:5000/api/stats?page=1&per_page=20&sort_by=clicks')
    .then(response => response.json())
    .then(data => console.log(data));
```

---

### 3. Get Specific URL Statistics

Get detailed statistics for a single shortened URL.

**Endpoint:** `GET /api/stats/<short_code>`

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| short_code | string | Yes | The short code of the URL |

**Success Response (200 OK):**
```json
{
    "id": 1,
    "original_url": "https://example.com/long-url",
    "short_code": "abc123",
    "short_url": "http://localhost:5000/abc123",
    "clicks": 42,
    "created_at": "2024-03-20 10:30:00",
    "expires_at": null,
    "custom": false
}
```

**Error Response (404 Not Found):**
```json
{
    "error": "Short URL not found"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/stats/abc123
```

---

### 4. Delete URL

Delete a shortened URL permanently.

**Endpoint:** `DELETE /api/delete/<short_code>`

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| short_code | string | Yes | The short code of the URL to delete |

**Success Response (200 OK):**
```json
{
    "message": "URL deleted successfully"
}
```

**Error Response (404 Not Found):**
```json
{
    "error": "Short URL not found"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/api/delete/abc123
```

**JavaScript Example:**
```javascript
fetch('http://localhost:5000/api/delete/abc123', {
    method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 5. Redirect to Original URL

Redirect to the original URL and increment the click counter.

**Endpoint:** `GET /<short_code>`

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| short_code | string | Yes | The short code to redirect |

**Success Response (302 Found):**
```http
HTTP/1.1 302 FOUND
Location: https://example.com/original-url
```

**Error Responses:**

```html
<!-- 404 Not Found - URL doesn't exist -->
404 page displayed

<!-- 410 Gone - URL expired -->
Expired page displayed
```

**cURL Example:**
```bash
curl -L http://localhost:5000/abc123
```

**Browser:**
Simply navigate to: `http://localhost:5000/abc123`

---

## ⚠️ Error Handling

All API endpoints return errors in a consistent JSON format:

```json
{
    "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 302 | Found | Redirect to original URL |
| 400 | Bad Request | Invalid input or parameters |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists (e.g., custom code taken) |
| 410 | Gone | Resource expired |
| 500 | Internal Server Error | Server-side error |

---

## 🔒 Rate Limiting

**Current Status:** No rate limiting implemented (suitable for development)

**Production Recommendation:** Implement rate limiting using Flask-Limiter

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@limiter.limit("10 per minute")
@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    # ... code
```

**Suggested Limits:**
- `/api/shorten`: 10 requests per minute per IP
- `/api/stats`: 30 requests per minute per IP
- `/<short_code>`: 100 requests per minute per IP

---

## 📝 Examples

### Complete Workflow Example (Python)

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Create a short URL
def create_short_url(long_url, custom_code=None):
    payload = {"url": long_url}
    if custom_code:
        payload["custom_code"] = custom_code
    
    response = requests.post(f"{BASE_URL}/api/shorten", json=payload)
    return response.json()

# 2. Get URL statistics
def get_stats(short_code):
    response = requests.get(f"{BASE_URL}/api/stats/{short_code}")
    return response.json()

# 3. Get all URLs
def get_all_urls(page=1, per_page=10):
    response = requests.get(f"{BASE_URL}/api/stats", params={
        "page": page,
        "per_page": per_page,
        "sort_by": "clicks",
        "order": "desc"
    })
    return response.json()

# 4. Delete URL
def delete_url(short_code):
    response = requests.delete(f"{BASE_URL}/api/delete/{short_code}")
    return response.json()

# Usage
if __name__ == "__main__":
    # Create URL
    result = create_short_url("https://www.google.com", "google")
    print(f"Short URL: {result['short_url']}")
    
    # Get stats
    stats = get_stats("google")
    print(f"Clicks: {stats['clicks']}")
    
    # Get all URLs
    all_urls = get_all_urls(page=1, per_page=20)
    print(f"Total URLs: {all_urls['total']}")
    
    # Delete URL
    # delete_result = delete_url("google")
    # print(delete_result['message'])
```

### Complete Workflow Example (JavaScript/Node.js)

```javascript
const BASE_URL = 'http://localhost:5000';

// 1. Create short URL
async function createShortUrl(longUrl, customCode = null) {
    const payload = { url: longUrl };
    if (customCode) payload.custom_code = customCode;
    
    const response = await fetch(`${BASE_URL}/api/shorten`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    return await response.json();
}

// 2. Get URL statistics
async function getStats(shortCode) {
    const response = await fetch(`${BASE_URL}/api/stats/${shortCode}`);
    return await response.json();
}

// 3. Get all URLs
async function getAllUrls(page = 1, perPage = 10) {
    const params = new URLSearchParams({
        page,
        per_page: perPage,
        sort_by: 'clicks',
        order: 'desc'
    });
    
    const response = await fetch(`${BASE_URL}/api/stats?${params}`);
    return await response.json();
}

// 4. Delete URL
async function deleteUrl(shortCode) {
    const response = await fetch(`${BASE_URL}/api/delete/${shortCode}`, {
        method: 'DELETE'
    });
    return await response.json();
}

// Usage
(async () => {
    // Create URL
    const result = await createShortUrl('https://www.google.com', 'google');
    console.log(`Short URL: ${result.short_url}`);
    
    // Get stats
    const stats = await getStats('google');
    console.log(`Clicks: ${stats.clicks}`);
    
    // Get all URLs
    const allUrls = await getAllUrls(1, 20);
    console.log(`Total URLs: ${allUrls.total}`);
})();
```

---

## 🧪 Testing the API

### Using cURL (Command Line)

```bash
# Create a short URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com"}'

# Create with custom code
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com","custom_code":"gh"}'

# Get all URLs
curl http://localhost:5000/api/stats

# Get specific URL stats
curl http://localhost:5000/api/stats/gh

# Delete URL
curl -X DELETE http://localhost:5000/api/delete/gh

# Test redirect (follow redirects)
curl -L http://localhost:5000/gh
```

### Using Postman

1. **Import Collection:**
   - Create requests for each endpoint
   - Save as collection for reuse

2. **Test Create URL:**
   ```
   POST http://localhost:5000/api/shorten
   Body (JSON):
   {
     "url": "https://example.com",
     "custom_code": "test"
   }
   ```

3. **Test Get Stats:**
   ```
   GET http://localhost:5000/api/stats?page=1&per_page=10
   ```

---

## 📱 Mobile App Integration

Example using React Native / Flutter:

```javascript
// React Native example
const shortenUrl = async (longUrl) => {
    try {
        const response = await fetch('https://your-app.com/api/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: longUrl })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            Alert.alert('Success', `Short URL: ${data.short_url}`);
            return data;
        } else {
            Alert.alert('Error', data.error);
        }
    } catch (error) {
        Alert.alert('Error', 'Network request failed');
    }
};
```

---

## 🔮 Future API Enhancements

Planned features for future versions:

- [ ] API key authentication
- [ ] User-specific URLs
- [ ] Webhook notifications on click events
- [ ] Batch URL shortening
- [ ] Advanced analytics (geolocation, devices, referrers)
- [ ] GraphQL API alternative
- [ ] WebSocket support for real-time updates

---

## 📞 API Support

For API-related questions or issues:
- Open an issue on GitHub
- Check the main README.md
- Review example code in this document

---

**Happy API Building! 🚀**
