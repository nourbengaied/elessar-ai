#!/usr/bin/env python3
"""
SAM Deployment Script for Parsea
Deploys the entire application using AWS SAM
"""

import os
import subprocess
import boto3
import json
from pathlib import Path

def check_prerequisites():
    """Check if SAM CLI and AWS CLI are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check SAM CLI
    try:
        result = subprocess.run(["sam", "--version"], capture_output=True, text=True)
        print(f"✅ SAM CLI: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ SAM CLI not found. Please install it first:")
        print("   https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html")
        return False
    
    # Check AWS CLI
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
        print(f"✅ AWS CLI: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ AWS CLI not found. Please install it first:")
        print("   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html")
        return False
    
    # Check AWS credentials
    try:
        boto3.client('sts').get_caller_identity()
        print("✅ AWS credentials verified")
    except Exception:
        print("❌ AWS credentials not found. Please configure AWS CLI first:")
        print("   aws configure")
        return False
    
    return True

def build_frontend():
    """Build the React frontend"""
    print("🔨 Building React frontend...")
    
    # Change to frontend directory
    os.chdir("frontend")
    
    # Install dependencies
    subprocess.run(["npm", "install"], check=True)
    
    # Build for production
    subprocess.run(["npm", "run", "build"], check=True)
    
    # Go back to root
    os.chdir("..")
    
    print("✅ Frontend built successfully!")

def deploy_with_sam(stack_name="parsea-stack", region="eu-west-2"):
    """Deploy the application using SAM"""
    print(f"🚀 Deploying with SAM to stack: {stack_name}")
    
    # Get JWT secret from environment or prompt user
    jwt_secret = os.getenv('JWT_SECRET')
    if not jwt_secret:
        jwt_secret = input("Enter JWT secret key: ")
    
    # Build SAM application
    print("📦 Building SAM application...")
    subprocess.run([
        "sam", "build",
        "--template-file", "template.yaml",
        "--use-container"
    ], check=True)
    
    # Deploy SAM application
    print("☁️ Deploying to AWS...")
    subprocess.run([
        "sam", "deploy",
        "--template-file", ".aws-sam/build/template.yaml",
        "--stack-name", stack_name,
        "--capabilities", "CAPABILITY_IAM",
        "--region", region,
        "--parameter-overrides", f"JWTSecret={jwt_secret}",
        "--resolve-s3",
        "--no-confirm-changeset",
        "--no-fail-on-empty-changeset"
    ], check=True)
    
    print("✅ SAM deployment completed!")

def deploy_frontend_to_s3(stack_name="parsea-stack"):
    """Deploy frontend to S3 bucket created by SAM"""
    print("📤 Deploying frontend to S3...")
    
    # Get S3 bucket name from CloudFormation outputs
    cloudformation = boto3.client('cloudformation')
    
    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0]['Outputs']
        
        s3_bucket = None
        for output in outputs:
            if output['OutputKey'] == 'S3Bucket':
                s3_bucket = output['OutputValue']
                break
        
        if not s3_bucket:
            print("❌ Could not find S3 bucket in CloudFormation outputs")
            return False
        
        print(f"📦 Found S3 bucket: {s3_bucket}")
        
        # Upload frontend files
        s3_client = boto3.client('s3')
        build_dir = Path("frontend/build")
        
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                s3_key = os.path.relpath(file_path, build_dir)
                
                # Set content type for different file types
                content_type = 'text/html' if file.endswith('.html') else \
                              'application/javascript' if file.endswith('.js') else \
                              'text/css' if file.endswith('.css') else \
                              'application/json' if file.endswith('.json') else \
                              'image/svg+xml' if file.endswith('.svg') else \
                              'binary/octet-stream'
                
                s3_client.upload_file(
                    file_path,
                    s3_bucket,
                    s3_key,
                    ExtraArgs={'ContentType': content_type}
                )
        
        print("✅ Frontend deployed to S3!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to deploy frontend: {e}")
        return False

def update_frontend_config(api_url):
    """Update frontend configuration with the deployed API URL"""
    print("🔧 Updating frontend API configuration...")
    
    config_file = "frontend/src/config/api.ts"
    
    try:
        # Read the current config
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Update the production API URL
        import re
        pattern = r"baseURL: process\.env\.REACT_APP_API_URL \|\| '[^']*'"
        replacement = f"baseURL: process.env.REACT_APP_API_URL || '{api_url}'"
        
        updated_content = re.sub(pattern, replacement, content)
        
        # Write back the updated config
        with open(config_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Frontend config updated with API URL: {api_url}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update frontend config: {e}")
        return False

def get_deployment_urls(stack_name="parsea-stack"):
    """Get deployment URLs from CloudFormation outputs"""
    print("🌐 Getting deployment URLs...")
    
    cloudformation = boto3.client('cloudformation')
    
    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0]['Outputs']
        
        api_url = None
        frontend_url = None
        
        for output in outputs:
            if output['OutputKey'] == 'ApiUrl':
                api_url = output['OutputValue']
            elif output['OutputKey'] == 'FrontendUrl':
                frontend_url = output['OutputValue']
        
        if api_url and frontend_url:
            print(f"✅ API URL: {api_url}")
            print(f"✅ Frontend URL: {frontend_url}")
            
            # Update frontend configuration
            update_frontend_config(api_url)
            
            return api_url, frontend_url
        else:
            print("❌ Could not find URLs in CloudFormation outputs")
            return None, None
            
    except Exception as e:
        print(f"❌ Failed to get deployment URLs: {e}")
        return None, None

def main():
    """Main deployment function"""
    print("🚀 Starting Parsea SAM deployment...")
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    # Build frontend
    build_frontend()
    
    # Deploy with SAM
    stack_name = "parsea-stack"
    region = "eu-west-2"
    
    try:
        deploy_with_sam(stack_name, region)
        
        # Deploy frontend to S3
        if deploy_frontend_to_s3(stack_name):
            # Get deployment URLs
            api_url, frontend_url = get_deployment_urls(stack_name)
            
            print("\n🎉 Deployment completed successfully!")
            print(f"\n📋 Deployment Information:")
            print(f"   Stack Name: {stack_name}")
            print(f"   Region: {region}")
            print(f"   API URL: {api_url}")
            print(f"   Frontend URL: {frontend_url}")
            print(f"\n⚠️ Note: CloudFront may take 10-15 minutes to fully deploy")
            
            # Save URLs to file
            with open("deployment-urls.json", "w") as f:
                json.dump({
                    "api_url": api_url,
                    "frontend_url": frontend_url,
                    "stack_name": stack_name,
                    "region": region
                }, f, indent=2)
            
            print(f"\n📄 URLs saved to: deployment-urls.json")
            
        else:
            print("❌ Frontend deployment failed!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ SAM deployment failed: {e}")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    main() 