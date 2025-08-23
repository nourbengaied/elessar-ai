#!/usr/bin/env python3
"""
Test registration and monitor logs for debugging
"""

import requests
import json
import sys
import time

# API endpoint from the deployment
API_URL = "https://nv9zp49sye.execute-api.eu-west-2.amazonaws.com/prod"

def test_registration():
    """Test user registration"""
    print("🧪 Testing registration...")
    
    # Test data - using unique email with timestamp
    import time
    timestamp = int(time.time())
    registration_data = {
        "email": f"test{timestamp}@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "business_name": "Test Business",
        "business_type": "Technology"
    }
    
    try:
        # Make registration request
        print(f"📤 Sending registration request to: {API_URL}/auth/register")
        response = requests.post(
            f"{API_URL}/auth/register",
            json=registration_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📄 Response Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"📄 Response Text: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_health_check():
    """Test basic health check"""
    print("🏥 Testing health check...")
    
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        print(f"📊 Health Check Status: {response.status_code}")
        print(f"📄 Health Check Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Parsea Registration Test")
    print("=" * 50)
    
    # Test health check first
    if test_health_check():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
    
    print("-" * 50)
    
    # Test registration
    if test_registration():
        print("✅ Registration test passed")
    else:
        print("❌ Registration test failed")
    
    print("\n💡 After running this, you can check logs with:")
    print("aws logs tail \"/aws/lambda/parsea-backend\" --region eu-west-2 --since 5m") 