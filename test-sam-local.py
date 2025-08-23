#!/usr/bin/env python3
"""
Local Testing Script for SAM Application
Tests the Lambda function locally before deployment
"""

import os
import subprocess
import json
import time
from pathlib import Path

def check_sam_cli():
    """Check if SAM CLI is installed"""
    try:
        result = subprocess.run(["sam", "--version"], capture_output=True, text=True)
        print(f"✅ SAM CLI: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ SAM CLI not found. Please install it first:")
        print("   https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html")
        return False

def build_sam_local():
    """Build SAM application for local testing"""
    print("🔨 Building SAM application for local testing...")
    
    subprocess.run([
        "sam", "build",
        "--template-file", "template.yaml",
        "--use-container"
    ], check=True)
    
    print("✅ SAM build completed!")

def start_local_api():
    """Start local API for testing"""
    print("🚀 Starting local API...")
    
    # Start SAM local API
    process = subprocess.Popen([
        "sam", "local", "start-api",
        "--template-file", ".aws-sam/build/template.yaml",
        "--port", "3001",
        "--host", "0.0.0.0"
    ])
    
    print("✅ Local API started on http://localhost:3001")
    print("📋 Available endpoints:")
    print("   - GET  /transactions/statistics/summary")
    print("   - GET  /transactions/")
    print("   - POST /transactions/upload")
    print("   - POST /auth/login")
    print("   - POST /auth/register")
    print("\n⏹️  Press Ctrl+C to stop the local API")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping local API...")
        process.terminate()
        process.wait()
        print("✅ Local API stopped")

def test_endpoints():
    """Test API endpoints locally"""
    print("🧪 Testing API endpoints...")
    
    import requests
    
    base_url = "http://localhost:3001"
    
    # Test endpoints
    endpoints = [
        ("GET", "/transactions/statistics/summary"),
        ("GET", "/transactions/"),
        ("POST", "/auth/login"),
    ]
    
    for method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            elif method == "POST":
                response = requests.post(f"{base_url}{endpoint}", json={})
            
            print(f"✅ {method} {endpoint}: {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint}: Connection failed (API not running)")
        except Exception as e:
            print(f"❌ {method} {endpoint}: {e}")

def create_test_events():
    """Create test event files for local testing"""
    print("📝 Creating test event files...")
    
    events_dir = Path("events")
    events_dir.mkdir(exist_ok=True)
    
    # Test event for statistics endpoint
    statistics_event = {
        "httpMethod": "GET",
        "path": "/transactions/statistics/summary",
        "headers": {
            "Content-Type": "application/json"
        },
        "queryStringParameters": None,
        "body": None
    }
    
    with open(events_dir / "statistics.json", "w") as f:
        json.dump(statistics_event, f, indent=2)
    
    # Test event for transactions endpoint
    transactions_event = {
        "httpMethod": "GET",
        "path": "/transactions/",
        "headers": {
            "Content-Type": "application/json"
        },
        "queryStringParameters": None,
        "body": None
    }
    
    with open(events_dir / "transactions.json", "w") as f:
        json.dump(transactions_event, f, indent=2)
    
    # Test event for login endpoint
    login_event = {
        "httpMethod": "POST",
        "path": "/auth/login",
        "headers": {
            "Content-Type": "application/json"
        },
        "queryStringParameters": None,
        "body": json.dumps({
            "email": "test@example.com",
            "password": "testpassword"
        })
    }
    
    with open(events_dir / "login.json", "w") as f:
        json.dump(login_event, f, indent=2)
    
    print("✅ Test event files created in events/ directory")

def invoke_function_locally(function_name="ParseaBackendFunction", event_file="events/statistics.json"):
    """Invoke Lambda function locally with test event"""
    print(f"🧪 Invoking function locally with {event_file}...")
    
    subprocess.run([
        "sam", "local", "invoke",
        function_name,
        "--template-file", ".aws-sam/build/template.yaml",
        "--event", event_file,
        "--env-vars", "env.json"
    ], check=True)

def main():
    """Main function"""
    print("🧪 SAM Local Testing")
    print("=" * 50)
    
    if not check_sam_cli():
        return
    
    # Create environment variables file
    env_vars = {
        "ParseaBackendFunction": {
            "ENVIRONMENT": "local",
            "DYNAMODB_TABLE": "parsea-transactions-local",
            "JWT_SECRET": "local-test-secret",
            "AWS_REGION": "us-east-1"
        }
    }
    
    with open("env.json", "w") as f:
        json.dump(env_vars, f, indent=2)
    
    # Build SAM application
    build_sam_local()
    
    # Create test events
    create_test_events()
    
    print("\n📋 Available commands:")
    print("1. Start local API: python test-sam-local.py --api")
    print("2. Test specific event: python test-sam-local.py --invoke events/statistics.json")
    print("3. Test all endpoints: python test-sam-local.py --test")
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--api":
            start_local_api()
        elif sys.argv[1] == "--invoke" and len(sys.argv) > 2:
            invoke_function_locally(event_file=sys.argv[2])
        elif sys.argv[1] == "--test":
            start_local_api()
            time.sleep(3)  # Wait for API to start
            test_endpoints()
    else:
        print("\n💡 Run with --api to start local API server")

if __name__ == "__main__":
    main() 