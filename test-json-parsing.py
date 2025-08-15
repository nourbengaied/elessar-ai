#!/usr/bin/env python3
"""
Test script for JSON parsing strategies
This helps debug why JSON might be getting cut off
"""

import json
import re
from typing import Dict, Any, List

def test_json_extraction_strategies(response_text: str):
    """Test all JSON extraction strategies on a sample response"""
    print("🔍 Testing JSON extraction strategies")
    print("=" * 50)
    print(f"Sample response text:\n{response_text}")
    print("\n" + "=" * 50)
    
    # Strategy 1: Look for JSON object with braces
    print("\n📋 Strategy 1: JSON object with braces")
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1
    
    if json_start != -1 and json_end > json_start:
        json_str = response_text[json_start:json_end]
        print(f"Found JSON at positions {json_start}:{json_end}")
        print(f"Extracted string: {json_str}")
        try:
            result = json.loads(json_str)
            print(f"✅ Strategy 1 successful: {result}")
        except json.JSONDecodeError as e:
            print(f"❌ Strategy 1 failed: {e}")
    else:
        print("❌ No JSON braces found")
    
    # Strategy 2: Look for JSON object with quotes and braces
    print("\n📋 Strategy 2: JSON object with quotes and braces")
    json_pattern = r'\{[^{}]*"[^"]*"[^{}]*\}'
    matches = re.findall(json_pattern, response_text)
    if matches:
        print(f"Found {len(matches)} potential JSON objects:")
        for i, match in enumerate(matches):
            print(f"  Match {i+1}: {match}")
            try:
                result = json.loads(match)
                print(f"  ✅ Valid JSON: {result}")
            except json.JSONDecodeError as e:
                print(f"  ❌ Invalid JSON: {e}")
    else:
        print("❌ No JSON patterns found")
    
    # Strategy 3: Manual construction
    print("\n📋 Strategy 3: Manual JSON construction")
    result = construct_json_from_text(response_text)
    if result:
        print(f"✅ Strategy 3 successful: {result}")
    else:
        print("❌ Strategy 3 failed")

def construct_json_from_text(text: str) -> Dict[str, Any]:
    """Manually construct JSON from text when parsing fails"""
    try:
        result = {}
        
        # Look for classification
        if 'business' in text.lower():
            result['classification'] = 'business'
        elif 'personal' in text.lower():
            result['classification'] = 'personal'
        else:
            result['classification'] = 'personal'
        
        # Look for confidence
        confidence_match = re.search(r'confidence[:\s]*(\d*\.?\d*)', text.lower())
        if confidence_match:
            try:
                result['confidence'] = float(confidence_match.group(1))
            except:
                result['confidence'] = 0.5
        else:
            result['confidence'] = 0.5
        
        # Look for reasoning
        reasoning_match = re.search(r'reasoning[:\s]*(.+?)(?=\n|$)', text.lower())
        if reasoning_match:
            result['reasoning'] = reasoning_match.group(1).strip()
        else:
            result['reasoning'] = 'Extracted from text analysis'
        
        # Look for category
        category_match = re.search(r'category[:\s]*(\w+)', text.lower())
        if category_match:
            result['category'] = category_match.group(1)
        else:
            result['category'] = 'unknown'
        
        return result
    except Exception as e:
        print(f"Error constructing JSON: {e}")
        return None

def test_transaction_extraction(response_text: str):
    """Test transaction extraction strategies"""
    print("\n🔍 Testing Transaction Extraction")
    print("=" * 50)
    
    # Strategy 1: JSON array
    print("\n📋 Strategy 1: JSON array extraction")
    json_start = response_text.find('[')
    json_end = response_text.rfind(']') + 1
    
    if json_start != -1 and json_end > json_start:
        json_str = response_text[json_start:json_end]
        print(f"Found array at positions {json_start}:{json_end}")
        print(f"Extracted string: {json_str}")
        try:
            result = json.loads(json_str)
            print(f"✅ Strategy 1 successful: {len(result)} transactions")
            for i, t in enumerate(result[:3]):  # Show first 3
                print(f"  Transaction {i+1}: {t}")
        except json.JSONDecodeError as e:
            print(f"❌ Strategy 1 failed: {e}")
    else:
        print("❌ No JSON array found")
    
    # Strategy 2: Multiple JSON objects
    print("\n📋 Strategy 2: Multiple JSON objects")
    json_objects = re.findall(r'\{[^{}]*"[^"]*"[^{}]*\}', response_text)
    if json_objects:
        print(f"Found {len(json_objects)} potential transaction objects:")
        for i, obj_str in enumerate(json_objects):
            try:
                obj = json.loads(obj_str)
                if 'date' in obj and 'description' in obj and 'amount' in obj:
                    print(f"  ✅ Valid transaction {i+1}: {obj}")
                else:
                    print(f"  ⚠️  Incomplete transaction {i+1}: {obj}")
            except json.JSONDecodeError as e:
                print(f"  ❌ Invalid JSON {i+1}: {e}")

if __name__ == "__main__":
    print("🧪 JSON Parsing Test Suite")
    print("=" * 50)
    
    # Test case 1: Good JSON response
    print("\n📝 Test Case 1: Good JSON Response")
    good_response = '{"classification": "business", "confidence": 0.85, "reasoning": "Office supplies", "category": "office_supplies"}'
    test_json_extraction_strategies(good_response)
    
    # Test case 2: JSON with extra text
    print("\n📝 Test Case 2: JSON with Extra Text")
    extra_text_response = '''Here is my analysis of the transaction:

The transaction appears to be a business expense because it's for office supplies.

{"classification": "business", "confidence": 0.85, "reasoning": "Office supplies for work", "category": "office_supplies"}

This classification is based on the merchant name and transaction description.'''
    test_json_extraction_strategies(extra_text_response)
    
    # Test case 3: Malformed JSON
    print("\n📝 Test Case 3: Malformed JSON")
    malformed_response = '''Here is my analysis:

{"classification": "business", "confidence": 0.85, "reasoning": "Office supplies for work", "category": "office_supplies"}

The transaction is clearly business-related.'''
    test_json_extraction_strategies(malformed_response)
    
    # Test case 4: Transaction array
    print("\n📝 Test Case 4: Transaction Array")
    transaction_response = '''I found the following transactions in your bank statement:

[
  {"date": "2024-01-15", "description": "Office supplies", "amount": -45.50, "currency": "USD", "merchant": "Office Depot"},
  {"date": "2024-01-16", "description": "Client payment", "amount": 1500.00, "currency": "USD", "merchant": "Client Corp"}
]

These transactions have been extracted and classified.'''
    test_transaction_extraction(transaction_response)
    
    print("\n✅ Test suite completed!") 