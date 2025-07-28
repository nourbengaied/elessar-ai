#!/usr/bin/env python3
"""
Test runner for Freelancer Transaction Classifier
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests"""
    print("Running tests for Freelancer Transaction Classifier...")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Run pytest
    result = subprocess.run([
        "python", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short"
    ], capture_output=True, text=True)
    
    # Print output
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 