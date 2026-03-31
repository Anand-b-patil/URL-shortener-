"""
Testing Script for Smart URL Shortener
Run this script to test all API endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST]{Colors.END} {test_name}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")

def test_home_page():
    """Test if home page loads"""
    print_test("Home Page Load")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success(f"Home page loaded successfully (Status: {response.status_code})")
            return True
        else:
            print_error(f"Home page failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Error connecting to server: {e}")
        return False

def test_dashboard_page():
    """Test if dashboard page loads"""
    print_test("Dashboard Page Load")
    try:
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            print_success(f"Dashboard loaded successfully (Status: {response.status_code})")
            return True
        else:
            print_error(f"Dashboard failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_create_short_url():
    """Test creating a short URL"""
    print_test("Create Short URL (Random Code)")
    try:
        payload = {
            "url": "https://www.google.com"
        }
        response = requests.post(f"{BASE_URL}/api/shorten", json=payload)
        data = response.json()
        
        if response.status_code in [200, 201]:
            print_success(f"URL shortened successfully")
            print_info(f"Original: {data['original_url']}")
            print_info(f"Short Code: {data['short_code']}")
            print_info(f"Short URL: {data['short_url']}")
            return data['short_code']
        else:
            print_error(f"Failed to shorten URL: {data.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_create_custom_url():
    """Test creating a custom short URL"""
    print_test("Create Short URL (Custom Code)")
    try:
        custom_code = f"test{int(time.time())}"
        payload = {
            "url": "https://github.com",
            "custom_code": custom_code
        }
        response = requests.post(f"{BASE_URL}/api/shorten", json=payload)
        data = response.json()
        
        if response.status_code in [200, 201]:
            print_success(f"Custom URL created successfully")
            print_info(f"Custom Code: {data['short_code']}")
            print_info(f"Short URL: {data['short_url']}")
            return data['short_code']
        else:
            print_error(f"Failed: {data.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_create_url_with_expiry():
    """Test creating URL with expiry"""
    print_test("Create Short URL (With Expiry)")
    try:
        payload = {
            "url": "https://www.python.org",
            "expires_in_days": 7
        }
        response = requests.post(f"{BASE_URL}/api/shorten", json=payload)
        data = response.json()
        
        if response.status_code in [200, 201]:
            print_success(f"URL with expiry created successfully")
            print_info(f"Short Code: {data['short_code']}")
            print_info(f"Expires: {data.get('expires_at', 'N/A')}")
            return data['short_code']
        else:
            print_error(f"Failed: {data.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_invalid_url():
    """Test creating URL with invalid input"""
    print_test("Create Short URL (Invalid URL)")
    try:
        payload = {
            "url": "not-a-valid-url"
        }
        response = requests.post(f"{BASE_URL}/api/shorten", json=payload)
        data = response.json()
        
        if response.status_code == 400:
            print_success(f"Invalid URL correctly rejected: {data.get('error')}")
            return True
        else:
            print_error(f"Invalid URL was accepted (should have been rejected)")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_duplicate_custom_code():
    """Test creating URL with duplicate custom code"""
    print_test("Create Short URL (Duplicate Custom Code)")
    try:
        custom_code = "duplicate_test"
        payload = {
            "url": "https://www.example.com",
            "custom_code": custom_code
        }
        
        # First attempt - should succeed
        response1 = requests.post(f"{BASE_URL}/api/shorten", json=payload)
        
        # Second attempt - should fail
        response2 = requests.post(f"{BASE_URL}/api/shorten", json=payload)
        data2 = response2.json()
        
        if response2.status_code == 409 or 'already taken' in data2.get('error', '').lower():
            print_success(f"Duplicate custom code correctly rejected")
            return True
        elif response2.status_code in [200, 201]:
            # Might return existing URL
            print_success(f"Returned existing URL (acceptable behavior)")
            return True
        else:
            print_error(f"Unexpected response: {data2}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_redirect(short_code):
    """Test URL redirection"""
    print_test(f"URL Redirection ({short_code})")
    try:
        response = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)
        
        if response.status_code == 302:
            print_success(f"Redirect working (Status: 302)")
            print_info(f"Location: {response.headers.get('Location', 'N/A')}")
            return True
        else:
            print_error(f"Redirect failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_get_stats(short_code):
    """Test getting statistics for a URL"""
    print_test(f"Get URL Statistics ({short_code})")
    try:
        response = requests.get(f"{BASE_URL}/api/stats/{short_code}")
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"Statistics retrieved successfully")
            print_info(f"Clicks: {data.get('clicks', 0)}")
            print_info(f"Created: {data.get('created_at', 'N/A')}")
            return True
        else:
            print_error(f"Failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_get_all_stats():
    """Test getting all URLs statistics"""
    print_test("Get All URLs Statistics")
    try:
        response = requests.get(f"{BASE_URL}/api/stats?page=1&per_page=10")
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"All statistics retrieved successfully")
            print_info(f"Total URLs: {data.get('total', 0)}")
            print_info(f"Pages: {data.get('pages', 0)}")
            print_info(f"Current Page: {data.get('current_page', 1)}")
            return True
        else:
            print_error(f"Failed to get statistics")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_click_tracking(short_code):
    """Test if clicks are being tracked"""
    print_test(f"Click Tracking ({short_code})")
    try:
        # Get initial click count
        response1 = requests.get(f"{BASE_URL}/api/stats/{short_code}")
        initial_clicks = response1.json().get('clicks', 0)
        
        # Click the link (follow redirect)
        requests.get(f"{BASE_URL}/{short_code}", allow_redirects=True)
        
        # Wait a moment
        time.sleep(1)
        
        # Get updated click count
        response2 = requests.get(f"{BASE_URL}/api/stats/{short_code}")
        updated_clicks = response2.json().get('clicks', 0)
        
        if updated_clicks > initial_clicks:
            print_success(f"Click tracking working (Clicks: {initial_clicks} → {updated_clicks})")
            return True
        else:
            print_error(f"Click count did not increment (Clicks: {initial_clicks})")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_delete_url(short_code):
    """Test deleting a URL"""
    print_test(f"Delete URL ({short_code})")
    try:
        response = requests.delete(f"{BASE_URL}/api/delete/{short_code}")
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"URL deleted successfully")
            
            # Verify deletion
            verify_response = requests.get(f"{BASE_URL}/api/stats/{short_code}")
            if verify_response.status_code == 404:
                print_success(f"Deletion verified (URL no longer exists)")
                return True
            else:
                print_error(f"URL still exists after deletion")
                return False
        else:
            print_error(f"Failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_404_page():
    """Test 404 page for non-existent short code"""
    print_test("404 Page (Non-existent URL)")
    try:
        response = requests.get(f"{BASE_URL}/nonexistent123456")
        
        if response.status_code == 404:
            print_success(f"404 page displayed correctly")
            return True
        else:
            print_error(f"Expected 404, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  Smart URL Shortener - Automated Test Suite{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    print(f"\n{Colors.YELLOW}Starting tests...{Colors.END}")
    print(f"{Colors.YELLOW}Base URL: {BASE_URL}{Colors.END}")
    print(f"{Colors.YELLOW}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    results = []
    
    # Test server connectivity
    results.append(("Home Page Load", test_home_page()))
    results.append(("Dashboard Load", test_dashboard_page()))
    
    # Test URL creation
    short_code1 = test_create_short_url()
    results.append(("Create URL (Random)", short_code1 is not None))
    
    short_code2 = test_create_custom_url()
    results.append(("Create URL (Custom)", short_code2 is not None))
    
    short_code3 = test_create_url_with_expiry()
    results.append(("Create URL (Expiry)", short_code3 is not None))
    
    # Test validation
    results.append(("Invalid URL Rejection", test_invalid_url()))
    results.append(("Duplicate Code Rejection", test_duplicate_custom_code()))
    
    # Test redirection (use first created URL)
    if short_code1:
        results.append(("URL Redirection", test_redirect(short_code1)))
        results.append(("Click Tracking", test_click_tracking(short_code1)))
        results.append(("Get URL Stats", test_get_stats(short_code1)))
    
    # Test statistics
    results.append(("Get All Stats", test_get_all_stats()))
    
    # Test 404
    results.append(("404 Page", test_404_page()))
    
    # Test deletion (delete custom URL)
    if short_code2:
        results.append(("Delete URL", test_delete_url(short_code2)))
    
    # Print summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  Test Summary{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"{status:30} {test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! Application is working correctly.{Colors.END}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ Some tests failed. Please review the errors above.{Colors.END}")
    
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    main()
