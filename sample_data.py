# =============================================================================
# SAMPLE DATA & TESTING UTILITIES
# Freelancer Transaction Classifier
# =============================================================================

# =============================================================================
# 1. SAMPLE CSV TEMPLATE
# =============================================================================

"""
SAMPLE CSV TEMPLATE (sample_transactions.csv):

date,description,amount,currency,merchant
2024-01-15,AMAZON.COM,45.67,USD,Amazon
2024-01-16,STARBUCKS,12.50,USD,Starbucks
2024-01-17,ADOBE SUBSCRIPTION,52.99,USD,Adobe
2024-01-18,UBER RIDE,25.00,USD,Uber
2024-01-19,OFFICE DEPOT,89.99,USD,Office Depot
2024-01-20,NETFLIX,15.99,USD,Netflix
2024-01-21,COWORKING SPACE,200.00,USD,WeWork
2024-01-22,GROCERY STORE,75.50,USD,Safeway
2024-01-23,CLOUD HOSTING,29.99,USD,AWS
2024-01-24,RESTAURANT,45.00,USD,Local Restaurant
"""

# =============================================================================
# 2. SAMPLE TRANSACTION DATA
# =============================================================================

SAMPLE_TRANSACTIONS = [
    {
        "date": "2024-01-15",
        "description": "AMAZON.COM",
        "amount": 45.67,
        "currency": "USD",
        "merchant": "Amazon",
        "expected_classification": "business",
        "expected_category": "office_supplies",
        "expected_confidence": 0.85
    },
    {
        "date": "2024-01-16",
        "description": "STARBUCKS",
        "amount": 12.50,
        "currency": "USD",
        "merchant": "Starbucks",
        "expected_classification": "personal",
        "expected_category": "food_beverages",
        "expected_confidence": 0.70
    },
    {
        "date": "2024-01-17",
        "description": "ADOBE SUBSCRIPTION",
        "amount": 52.99,
        "currency": "USD",
        "merchant": "Adobe",
        "expected_classification": "business",
        "expected_category": "software_subscription",
        "expected_confidence": 0.95
    },
    {
        "date": "2024-01-18",
        "description": "UBER RIDE",
        "amount": 25.00,
        "currency": "USD",
        "merchant": "Uber",
        "expected_classification": "personal",
        "expected_category": "transportation",
        "expected_confidence": 0.80
    },
    {
        "date": "2024-01-19",
        "description": "OFFICE DEPOT",
        "amount": 89.99,
        "currency": "USD",
        "merchant": "Office Depot",
        "expected_classification": "business",
        "expected_category": "office_supplies",
        "expected_confidence": 0.90
    },
    {
        "date": "2024-01-20",
        "description": "NETFLIX",
        "amount": 15.99,
        "currency": "USD",
        "merchant": "Netflix",
        "expected_classification": "personal",
        "expected_category": "entertainment",
        "expected_confidence": 0.95
    },
    {
        "date": "2024-01-21",
        "description": "COWORKING SPACE",
        "amount": 200.00,
        "currency": "USD",
        "merchant": "WeWork",
        "expected_classification": "business",
        "expected_category": "office_rent",
        "expected_confidence": 0.98
    },
    {
        "date": "2024-01-22",
        "description": "GROCERY STORE",
        "amount": 75.50,
        "currency": "USD",
        "merchant": "Safeway",
        "expected_classification": "personal",
        "expected_category": "groceries",
        "expected_confidence": 0.85
    },
    {
        "date": "2024-01-23",
        "description": "CLOUD HOSTING",
        "amount": 29.99,
        "currency": "USD",
        "merchant": "AWS",
        "expected_classification": "business",
        "expected_category": "hosting_infrastructure",
        "expected_confidence": 0.95
    },
    {
        "date": "2024-01-24",
        "description": "RESTAURANT",
        "amount": 45.00,
        "currency": "USD",
        "merchant": "Local Restaurant",
        "expected_classification": "personal",
        "expected_category": "dining",
        "expected_confidence": 0.75
    }
]

# =============================================================================
# 3. BUSINESS EXPENSE CATEGORIES
# =============================================================================

BUSINESS_EXPENSE_CATEGORIES = {
    "office_supplies": [
        "Amazon", "Office Depot", "Staples", "Target", "Walmart",
        "paper", "pens", "notebooks", "printer", "ink", "stapler"
    ],
    "software_subscription": [
        "Adobe", "Microsoft", "Slack", "Zoom", "Trello", "Asana",
        "subscription", "software", "license", "app"
    ],
    "hosting_infrastructure": [
        "AWS", "Google Cloud", "Azure", "DigitalOcean", "Heroku",
        "hosting", "server", "domain", "SSL", "cloud"
    ],
    "office_rent": [
        "WeWork", "Regus", "Spaces", "coworking", "office space",
        "rent", "lease", "workspace"
    ],
    "travel": [
        "Uber", "Lyft", "taxi", "flight", "hotel", "airbnb",
        "travel", "transportation", "mileage"
    ],
    "meals_entertainment": [
        "restaurant", "lunch", "dinner", "client meal", "business lunch",
        "entertainment", "client entertainment"
    ],
    "marketing": [
        "Google Ads", "Facebook Ads", "LinkedIn Ads", "marketing",
        "advertising", "promotion", "SEO", "social media"
    ],
    "professional_development": [
        "course", "training", "conference", "workshop", "certification",
        "education", "learning", "skill development"
    ],
    "insurance": [
        "insurance", "liability", "professional liability", "business insurance",
        "coverage", "policy"
    ],
    "utilities": [
        "internet", "phone", "electricity", "water", "gas",
        "utility", "service", "bill"
    ]
}

# =============================================================================
# 4. PERSONAL EXPENSE CATEGORIES
# =============================================================================

PERSONAL_EXPENSE_CATEGORIES = {
    "groceries": [
        "Safeway", "Kroger", "Whole Foods", "Trader Joe's", "grocery",
        "food", "supermarket", "market"
    ],
    "dining": [
        "restaurant", "cafe", "fast food", "pizza", "sushi",
        "dining", "eating out", "takeout"
    ],
    "entertainment": [
        "Netflix", "Hulu", "Disney+", "Spotify", "Apple Music",
        "movie", "game", "entertainment", "streaming"
    ],
    "transportation": [
        "Uber", "Lyft", "taxi", "gas", "parking", "public transit",
        "transportation", "commute"
    ],
    "shopping": [
        "Amazon", "Target", "Walmart", "mall", "clothing", "shoes",
        "shopping", "retail", "store"
    ],
    "healthcare": [
        "pharmacy", "doctor", "dentist", "hospital", "medical",
        "healthcare", "medicine", "prescription"
    ],
    "utilities": [
        "electricity", "water", "gas", "internet", "phone",
        "utility", "bill", "service"
    ],
    "housing": [
        "rent", "mortgage", "home improvement", "furniture",
        "housing", "accommodation", "residence"
    ],
    "personal_care": [
        "salon", "spa", "gym", "fitness", "beauty", "cosmetics",
        "personal care", "wellness"
    ],
    "education": [
        "university", "college", "school", "course", "book",
        "education", "learning", "tuition"
    ]
}

# =============================================================================
# 5. TESTING UTILITIES
# =============================================================================

import csv
import io
from typing import List, Dict, Any

def create_sample_csv(transactions: List[Dict[str, Any]]) -> str:
    """
    Create a CSV string from transaction data
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['date', 'description', 'amount', 'currency', 'merchant'])
    
    # Write transactions
    for transaction in transactions:
        writer.writerow([
            transaction['date'],
            transaction['description'],
            transaction['amount'],
            transaction.get('currency', 'USD'),
            transaction.get('merchant', '')
        ])
    
    return output.getvalue()

def generate_test_transactions(count: int = 10) -> List[Dict[str, Any]]:
    """
    Generate random test transactions
    """
    import random
    from datetime import datetime, timedelta
    
    merchants = [
        "Amazon", "Starbucks", "Adobe", "Uber", "Office Depot",
        "Netflix", "WeWork", "Safeway", "AWS", "Local Restaurant",
        "Google", "Microsoft", "Slack", "Zoom", "Trello"
    ]
    
    descriptions = [
        "AMAZON.COM", "STARBUCKS", "ADOBE SUBSCRIPTION", "UBER RIDE",
        "OFFICE DEPOT", "NETFLIX", "COWORKING SPACE", "GROCERY STORE",
        "CLOUD HOSTING", "RESTAURANT", "GOOGLE ADS", "MICROSOFT 365",
        "SLACK SUBSCRIPTION", "ZOOM PRO", "TRELLO PREMIUM"
    ]
    
    transactions = []
    base_date = datetime.now() - timedelta(days=count)
    
    for i in range(count):
        transaction = {
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "description": random.choice(descriptions),
            "amount": round(random.uniform(10.0, 200.0), 2),
            "currency": "USD",
            "merchant": random.choice(merchants)
        }
        transactions.append(transaction)
    
    return transactions

def validate_csv_format(csv_content: str) -> bool:
    """
    Validate CSV format and required columns
    """
    try:
        csv_reader = csv.reader(io.StringIO(csv_content))
        header = next(csv_reader)
        
        required_columns = ['date', 'description', 'amount']
        missing_columns = [col for col in required_columns if col not in header]
        
        if missing_columns:
            return False
        
        # Check if there's at least one data row
        for row in csv_reader:
            if len(row) >= 3:  # date, description, amount
                return True
        
        return False
        
    except Exception:
        return False

def calculate_classification_accuracy(predictions: List[Dict], 
                                   actuals: List[Dict]) -> Dict[str, float]:
    """
    Calculate classification accuracy metrics
    """
    total = len(predictions)
    correct = 0
    business_correct = 0
    personal_correct = 0
    business_total = 0
    personal_total = 0
    
    for pred, actual in zip(predictions, actuals):
        if pred['classification'] == actual['expected_classification']:
            correct += 1
            
            if actual['expected_classification'] == 'business':
                business_correct += 1
            else:
                personal_correct += 1
        
        if actual['expected_classification'] == 'business':
            business_total += 1
        else:
            personal_total += 1
    
    return {
        "overall_accuracy": correct / total if total > 0 else 0,
        "business_accuracy": business_correct / business_total if business_total > 0 else 0,
        "personal_accuracy": personal_correct / personal_total if personal_total > 0 else 0,
        "total_transactions": total
    }

# =============================================================================
# 6. EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Create sample CSV
    csv_content = create_sample_csv(SAMPLE_TRANSACTIONS)
    print("Sample CSV Content:")
    print(csv_content)
    
    # Generate random test data
    test_transactions = generate_test_transactions(5)
    print("\nRandom Test Transactions:")
    for transaction in test_transactions:
        print(f"{transaction['date']}: {transaction['description']} - ${transaction['amount']}")
    
    # Validate CSV format
    is_valid = validate_csv_format(csv_content)
    print(f"\nCSV Format Valid: {is_valid}")
    
    # Example classification accuracy calculation
    predictions = [
        {"classification": "business", "confidence": 0.85},
        {"classification": "personal", "confidence": 0.70},
        {"classification": "business", "confidence": 0.95}
    ]
    
    actuals = [
        {"expected_classification": "business"},
        {"expected_classification": "personal"},
        {"expected_classification": "business"}
    ]
    
    accuracy = calculate_classification_accuracy(predictions, actuals)
    print(f"\nClassification Accuracy: {accuracy}")

# =============================================================================
# 7. PERFORMANCE TESTING DATA
# =============================================================================

PERFORMANCE_TEST_DATA = {
    "small_batch": generate_test_transactions(10),
    "medium_batch": generate_test_transactions(100),
    "large_batch": generate_test_transactions(1000),
    "mixed_transactions": [
        # Business expenses
        {"date": "2024-01-01", "description": "ADOBE CREATIVE SUITE", "amount": 52.99, "merchant": "Adobe"},
        {"date": "2024-01-02", "description": "AWS CLOUD SERVICES", "amount": 89.50, "merchant": "AWS"},
        {"date": "2024-01-03", "description": "OFFICE SUPPLIES", "amount": 125.00, "merchant": "Office Depot"},
        {"date": "2024-01-04", "description": "COWORKING SPACE", "amount": 300.00, "merchant": "WeWork"},
        {"date": "2024-01-05", "description": "PROFESSIONAL LIABILITY INSURANCE", "amount": 150.00, "merchant": "Insurance Co"},
        
        # Personal expenses
        {"date": "2024-01-06", "description": "NETFLIX SUBSCRIPTION", "amount": 15.99, "merchant": "Netflix"},
        {"date": "2024-01-07", "description": "GROCERY SHOPPING", "amount": 85.50, "merchant": "Safeway"},
        {"date": "2024-01-08", "description": "RESTAURANT DINNER", "amount": 65.00, "merchant": "Local Restaurant"},
        {"date": "2024-01-09", "description": "GAS STATION", "amount": 45.00, "merchant": "Shell"},
        {"date": "2024-01-10", "description": "MOVIE THEATER", "amount": 25.00, "merchant": "AMC"}
    ]
}

# =============================================================================
# 8. EDGE CASES FOR TESTING
# =============================================================================

EDGE_CASE_TRANSACTIONS = [
    # Ambiguous cases
    {
        "date": "2024-01-15",
        "description": "COFFEE SHOP",
        "amount": 8.50,
        "merchant": "Starbucks",
        "note": "Could be business meeting or personal"
    },
    {
        "date": "2024-01-16",
        "description": "UBER RIDE",
        "amount": 35.00,
        "merchant": "Uber",
        "note": "Could be client meeting or personal travel"
    },
    
    # High amounts
    {
        "date": "2024-01-17",
        "description": "LAPTOP PURCHASE",
        "amount": 1500.00,
        "merchant": "Apple Store",
        "note": "Large purchase - likely business"
    },
    
    # Small amounts
    {
        "date": "2024-01-18",
        "description": "PEN PURCHASE",
        "amount": 2.99,
        "merchant": "Office Depot",
        "note": "Small amount but business related"
    },
    
    # Unclear descriptions
    {
        "date": "2024-01-19",
        "description": "PAYMENT",
        "amount": 100.00,
        "merchant": "Unknown",
        "note": "Vague description"
    },
    
    # International transactions
    {
        "date": "2024-01-20",
        "description": "HOTEL BOOKING",
        "amount": 200.00,
        "currency": "EUR",
        "merchant": "Booking.com",
        "note": "International travel - could be business or personal"
    }
]

# =============================================================================
# SAMPLE DATA COMPLETE
# =============================================================================
# 
# This file provides comprehensive sample data and testing utilities for
# the freelancer transaction classifier. Use these for:
#
# 1. Testing CSV upload functionality
# 2. Validating LLM classification accuracy
# 3. Performance testing with different batch sizes
# 4. Edge case testing
# 5. Development and debugging
#
# Key features:
# - Realistic transaction data
# - Business vs personal categorization
# - Multiple currencies and amounts
# - Edge cases and ambiguous transactions
# - Performance testing datasets
# - Validation utilities
#
# ============================================================================= 