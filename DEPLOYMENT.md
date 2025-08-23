# 🚀 Parsea AWS Deployment Guide

## Architecture Overview

```
Frontend (React) → S3 + CloudFront
Backend (FastAPI) → Lambda + API Gateway
Database → DynamoDB
```

## 📋 Prerequisites

1. **AWS CLI configured** with appropriate permissions
2. **SAM CLI installed** (recommended)
3. **Python 3.11+** installed
4. **Node.js 16+** installed
5. **Docker** (for SAM local testing)

## 🛠️ Setup Steps

### 1. Install Dependencies

```bash
# Install SAM CLI
# macOS:
brew install aws/tap/aws-sam-cli

# Linux:
pip install aws-sam-cli

# Windows:
# Download from https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

# Install Python dependencies
pip install boto3 mangum

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 2. Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
```

### 3. Set Environment Variables

```bash
export JWT_SECRET="your-super-secret-jwt-key"
export AWS_REGION="us-east-1"
```

## 🚀 Deployment Options

### Option A: SAM Deployment (Recommended)

#### Quick Deploy:
```bash
python deploy-sam.py
```

#### Manual SAM Deploy:
```bash
# Build the application
sam build --use-container

# Deploy to AWS
sam deploy --guided
```

### Option B: Local Testing First

#### Test Locally:
```bash
# Build and start local API
python test-sam-local.py --api

# Test specific endpoints
python test-sam-local.py --invoke events/statistics.json

# Test all endpoints
python test-sam-local.py --test
```

### Option C: Manual Scripts (Legacy)

#### Deploy Backend:
```bash
python deploy-lambda.py
```

#### Deploy Frontend:
```bash
python deploy-frontend.py
```

## 📊 Cost Breakdown

### Monthly Costs (Estimated):
- **Lambda**: $0.01-0.10/month
- **S3**: $0.001/month
- **CloudFront**: $0.09/month
- **DynamoDB**: $0.26/month
- **API Gateway**: $0.01/month
- **Total**: **~$0.36/month** 🎉

## 🔧 Configuration Details

### SAM Template (`template.yaml`):
- **Lambda Function**: 1024MB RAM, 300s timeout
- **API Gateway**: CORS enabled, proxy integration
- **DynamoDB**: Pay-per-request billing
- **S3**: Static website hosting
- **CloudFront**: Global CDN with SPA routing

### Lambda Configuration:
- **Runtime**: Python 3.11
- **Memory**: 1024 MB
- **Timeout**: 300 seconds (5 minutes)
- **Handler**: `lambda_handler.lambda_handler`

### DynamoDB Table:
- **Name**: `parsea-transactions`
- **Billing**: Pay-per-request
- **Keys**: 
  - Partition Key: `id` (String)
  - Sort Key: `user_id` (String)

## 🔄 Update Process

### Backend Updates:
```bash
# Make code changes
# Deploy with SAM
python deploy-sam.py
```

### Frontend Updates:
```bash
# Make code changes
# Deploy with SAM (includes frontend)
python deploy-sam.py
```

### Manual Updates:
```bash
# Build and deploy
sam build --use-container
sam deploy
```

## 🧪 Local Testing

### Start Local API:
```bash
python test-sam-local.py --api
```

### Test Specific Function:
```bash
python test-sam-local.py --invoke events/login.json
```

### Test All Endpoints:
```bash
python test-sam-local.py --test
```

## 🐛 Troubleshooting

### Common Issues:

#### 1. SAM Build Failures
- **Issue**: Docker not running or SAM CLI not installed
- **Solution**: Install Docker and SAM CLI, ensure Docker is running

#### 2. Lambda Cold Starts
- **Issue**: 3-5 second delays on first request
- **Solution**: Consider using Provisioned Concurrency for production

#### 3. File Upload Timeouts
- **Issue**: Large files timeout during processing
- **Solution**: Increase Lambda timeout in template.yaml

#### 4. CORS Issues
- **Issue**: Frontend can't call API
- **Solution**: CORS is configured in SAM template

#### 5. DynamoDB Connection Issues
- **Issue**: Lambda can't connect to DynamoDB
- **Solution**: IAM permissions are configured in SAM template

## 📈 Scaling Considerations

### For Higher Traffic:
1. **Lambda**: Increase memory allocation in template.yaml
2. **DynamoDB**: Add read/write capacity
3. **CloudFront**: Already scales automatically
4. **API Gateway**: Add throttling if needed

### Cost Optimization:
1. **Lambda**: Use provisioned concurrency for consistent performance
2. **DynamoDB**: Use on-demand billing for unpredictable traffic
3. **CloudFront**: Monitor data transfer costs

## 🔒 Security Best Practices

1. **JWT Secret**: Use a strong, random secret
2. **IAM Roles**: SAM automatically creates least-privilege roles
3. **CORS**: Configure specific origins in production
4. **HTTPS**: All traffic uses HTTPS
5. **Environment Variables**: Never commit secrets to code

## 📞 Support

For deployment issues:
1. Check CloudFormation stack events
2. Verify IAM permissions
3. Test locally with SAM
4. Review CloudWatch logs

## 🎯 Next Steps

After successful deployment:
1. Update frontend API endpoint
2. Test all functionality
3. Set up monitoring and alerts
4. Configure custom domain (optional)
5. Set up CI/CD pipeline (optional)

## 📁 Project Structure

```
parsea/
├── template.yaml              # SAM template
├── deploy-sam.py              # SAM deployment script
├── test-sam-local.py          # Local testing script
├── backend/
│   ├── lambda_handler.py      # Lambda entry point
│   ├── requirements-lambda.txt # Lambda dependencies
│   └── app/                   # FastAPI application
├── frontend/                  # React application
├── events/                    # Test event files
└── deployment-urls.json       # Generated deployment URLs
``` 