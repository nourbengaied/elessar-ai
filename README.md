# Freelancer Transaction Classifier

An LLM-powered system to help freelancers automatically classify their bank transactions as either business expenses or personal expenses using **AWS Bedrock**.

## Features

- **AWS Bedrock Integration**: Uses Claude 3 Sonnet for intelligent transaction classification
- **CSV Upload**: Simple CSV upload for bank statement processing
- **Confidence Scoring**: Each classification comes with a confidence score (0.0-1.0)
- **Manual Override**: Users can correct misclassifications and the system learns from feedback
- **Export Functionality**: Export classified transactions for tax preparation
- **Multi-Currency Support**: Handles transactions in different currencies
- **Secure Authentication**: JWT-based authentication with proper security measures
- **RESTful API**: Complete FastAPI backend with comprehensive endpoints
- **Modern Frontend**: React-based web interface with beautiful UI/UX

## Architecture

### Backend (FastAPI + PostgreSQL)
- **Models**: SQLAlchemy models for users, transactions, and classifications
- **Services**: Business logic for transaction processing and AWS Bedrock integration
- **API**: RESTful endpoints for all functionality
- **Security**: JWT authentication and data encryption

### Frontend (React + TypeScript)
- **Modern UI**: Built with Tailwind CSS and React
- **Authentication**: Secure login and registration
- **Dashboard**: Statistics and charts for data visualization
- **Transaction Management**: View, filter, and edit classifications
- **File Upload**: Drag-and-drop CSV upload interface
- **Reports**: Export functionality with multiple formats

### AWS Bedrock Integration
- **Model**: Claude 3 Sonnet (anthropic.claude-3-sonnet-20240229-v1:0)
- **Prompt Engineering**: Sophisticated prompts for accurate classification
- **Error Handling**: Robust error handling for API failures
- **Response Parsing**: Intelligent JSON parsing with fallbacks

## Project Structure

```
freelancer_transaction_classifier/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # Database connection
│   │   ├── models/                 # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── transaction.py
│   │   │   └── classification.py
│   │   ├── api/                    # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── transactions.py
│   │   │   └── export.py
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── bedrock_service.py  # AWS Bedrock integration
│   │   │   ├── transaction_service.py
│   │   │   └── export_service.py
│   │   └── utils/                  # Utility functions
│   │       ├── __init__.py
│   │       ├── security.py
│   │       └── validators.py
│   ├── tests/                      # Test files
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── pages/                  # Page components
│   │   ├── contexts/               # React contexts
│   │   ├── services/               # API services
│   │   └── App.tsx                 # Main app component
│   ├── package.json
│   └── README.md
├── docker-compose.yml
├── env.example
├── run_tests.py
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database
- AWS account with Bedrock access
- Docker (for containerized deployment)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd freelancer_transaction_classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Configure Environment

```bash
# Copy environment file
cp env.example .env

# Edit .env with your settings
nano .env
```

### 3. Start the Application

**Option A: Using Docker Compose (Recommended)**
```bash
docker-compose up --build
```

**Option B: Local Development**
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd frontend
npm start
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/freelancer_classifier

# Security
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# File Upload Configuration
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.csv

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO
```

### AWS Bedrock Setup

1. **Create AWS Account**: Sign up for AWS if you don't have one
2. **Enable Bedrock**: Go to AWS Bedrock console and enable the service
3. **Create IAM User**: Create an IAM user with Bedrock permissions
4. **Get Credentials**: Generate access keys for the IAM user
5. **Update Environment**: Add your AWS credentials to the `.env` file

## Usage

### 1. Register/Login
- Create an account or login to the application
- Provide your business information for better classification

### 2. Upload Transactions
- Prepare a CSV file with your transactions
- Use the drag-and-drop interface to upload
- The system will automatically classify each transaction

### 3. Review Classifications
- View all transactions with their AI classifications
- Check confidence scores for each classification
- Manually override incorrect classifications

### 4. Generate Reports
- Export all transactions
- Generate business expense reports
- Create tax-ready reports for specific years

## Testing

### Backend Tests
```bash
# Run all tests
python run_tests.py

# Run specific test file
pytest backend/tests/test_transactions.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# View logs
docker-compose logs -f
```

### Production Considerations

1. **Security**:
   - Change default secret keys
   - Use HTTPS in production
   - Configure proper CORS settings
   - Set up proper database credentials

2. **Performance**:
   - Use a production database (RDS, etc.)
   - Configure proper logging
   - Set up monitoring and alerts

3. **Scalability**:
   - Use load balancers
   - Configure auto-scaling
   - Set up CDN for static assets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section below

## Troubleshooting

### Common Issues

1. **AWS Bedrock Access Denied**
   - Verify your AWS credentials
   - Check IAM permissions for Bedrock
   - Ensure Bedrock is enabled in your region

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database exists

3. **Frontend Not Loading**
   - Check if backend is running
   - Verify CORS settings
   - Check browser console for errors

4. **File Upload Fails**
   - Check file size limits
   - Verify CSV format
   - Check file permissions

### Debug Mode

Enable debug mode in your `.env` file:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

This will provide more detailed error messages and logging. 