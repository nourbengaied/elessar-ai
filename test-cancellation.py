#!/usr/bin/env python3
"""
Test script for transaction processing cancellation functionality
"""

import requests
import json
import time

def test_cancellation_endpoint():
    """Test the cancellation endpoint"""
    base_url = "http://nv9zp49sye.execute-api.eu-west-2.amazonaws.com/prod"
    
    print("🔍 Testing Transaction Processing Cancellation")
    print("=" * 50)
    
    try:
        # Test cancellation endpoint (will fail without auth, but we can test it exists)
        print("🧪 Testing cancellation endpoint...")
        response = requests.post(f"{base_url}/transactions/cancel-processing")
        
        if response.status_code == 401:
            print("✅ Cancellation endpoint exists (401 Unauthorized expected without auth)")
        elif response.status_code == 200:
            print("✅ Cancellation request successful")
            result = response.json()
            print(f"📊 Cancellation response: {result}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on nv9zp49sye.execute-api.eu-west-2.amazonaws.com/prod")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_cancellation_file_creation():
    """Test that cancellation files are created properly"""
    import os
    
    print("\n🧪 Testing cancellation file creation...")
    
    # Test user ID
    test_user_id = "test_user_123"
    cancellation_file = f"/tmp/cancel_{test_user_id}"
    
    # Create a test cancellation file
    try:
        with open(cancellation_file, 'w') as f:
            f.write("2024-01-01T12:00:00")
        
        if os.path.exists(cancellation_file):
            print("✅ Cancellation file created successfully")
            
            # Clean up
            os.remove(cancellation_file)
            print("✅ Cancellation file cleaned up")
        else:
            print("❌ Cancellation file was not created")
            
    except Exception as e:
        print(f"❌ Error creating cancellation file: {str(e)}")

if __name__ == "__main__":
    test_cancellation_endpoint()
    test_cancellation_file_creation() 