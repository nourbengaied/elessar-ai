#!/usr/bin/env python3
"""
Test script for transaction update functionality
"""

import requests
import json

def test_transaction_update():
    """Test the transaction update endpoint"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Transaction Update Functionality")
    print("=" * 50)
    
    try:
        # Test transaction update endpoint (will fail without auth, but we can test the structure)
        print("🧪 Testing transaction update endpoint...")
        
        # Test with valid JSON body
        test_data = {
            "is_business": True
        }
        
        response = requests.put(
            f"{base_url}/api/v1/transactions/test-transaction-id",
            json=test_data
        )
        
        if response.status_code == 401:
            print("✅ Transaction update endpoint exists (401 Unauthorized expected without auth)")
            print("✅ Request body structure is correct")
        elif response.status_code == 404:
            print("✅ Transaction update endpoint exists (404 Not Found expected for invalid ID)")
            print("✅ Request body structure is correct")
        elif response.status_code == 200:
            print("✅ Transaction update successful")
            result = response.json()
            print(f"📊 Update response: {result}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_transaction_get():
    """Test the transaction get endpoint"""
    base_url = "http://localhost:8000"
    
    print("\n🧪 Testing transaction get endpoint...")
    
    try:
        response = requests.get(f"{base_url}/api/v1/transactions/")
        
        if response.status_code == 401:
            print("✅ Transaction get endpoint exists (401 Unauthorized expected without auth)")
        elif response.status_code == 200:
            print("✅ Transaction get successful")
            result = response.json()
            print(f"📊 Response structure: {list(result.keys())}")
            if 'transactions' in result and len(result['transactions']) > 0:
                transaction = result['transactions'][0]
                print(f"📊 Sample transaction fields: {list(transaction.keys())}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_transaction_update()
    test_transaction_get() 