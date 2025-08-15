#!/usr/bin/env python3
"""
Test script for clear all transactions functionality
"""

import requests
import json

def test_clear_all_transactions():
    """Test the clear all transactions endpoint"""
    base_url = "http://localhost:8000"
    
    # First, let's get the current transactions
    print("🔍 Testing Clear All Transactions Functionality")
    print("=" * 50)
    
    try:
        # Get current transactions
        response = requests.get(f"{base_url}/api/v1/transactions/")
        if response.status_code == 200:
            transactions = response.json()
            print(f"📊 Current transactions: {len(transactions.get('transactions', []))}")
        else:
            print(f"❌ Failed to get transactions: {response.status_code}")
            return
        
        # Test clear all transactions (this will fail without auth, but we can test the endpoint exists)
        print("\n🧪 Testing clear all transactions endpoint...")
        response = requests.delete(f"{base_url}/api/v1/transactions/")
        
        if response.status_code == 401:
            print("✅ Endpoint exists (401 Unauthorized expected without auth)")
        elif response.status_code == 200:
            print("✅ Clear all transactions successful")
            result = response.json()
            print(f"📊 Deleted {result.get('deleted_count', 0)} transactions")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_clear_all_transactions() 