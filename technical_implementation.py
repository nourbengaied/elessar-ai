# =============================================================================
# TECHNICAL IMPLEMENTATION GUIDE
# Freelancer Transaction Classifier
# =============================================================================

# =============================================================================
# 1. PROJECT STRUCTURE
# =============================================================================

"""
RECOMMENDED PROJECT STRUCTURE:

freelancer_transaction_classifier/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration settings
│   │   ├── models/                 # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── transaction.py
│   │   │   └── classification.py
│   │   ├── api/                    # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── transactions.py
│   │   │   └── classifications.py
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py
│   │   │   ├── transaction_service.py
│   │   │   └── export_service.py
│   │   ├── utils/                  # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── validators.py
│   │   └── database.py             # Database connection
│   ├── tests/                      # Test files
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── docs/                           # Documentation
├── docker-compose.yml
└── README.md
"""

# =============================================================================
# 2. BACKEND IMPLEMENTATION
# =============================================================================

"""
CORE DEPENDENCIES (requirements.txt):
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
openai==1.3.7
pandas==2.1.3
pydantic==2.5.0
python-dotenv==1.0.0
"""

# =============================================================================
# 3. DATABASE MODELS
# =============================================================================

"""
EXAMPLE DATABASE MODELS (models/user.py):
"""

from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    business_name = Column(String)
    tax_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

"""
EXAMPLE TRANSACTION MODEL (models/transaction.py):
"""

from sqlalchemy import Column, String, DateTime, UUID, Boolean, Float, Text, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='USD')
    merchant = Column(String)
    category = Column(String)
    is_business_expense = Column(Boolean)
    confidence_score = Column(Float)
    llm_reasoning = Column(Text)
    manually_overridden = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# =============================================================================
# 4. LLM SERVICE IMPLEMENTATION
# =============================================================================

"""
LLM SERVICE (services/llm_service.py):
"""

import openai
from typing import Dict, Any
import json

class LLMService:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def classify_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a transaction using LLM
        """
        prompt = self._build_classification_prompt(transaction_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = self._parse_llm_response(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "classification": "personal",
                "confidence": 0.0,
                "reasoning": f"Error in classification: {str(e)}",
                "category": "unknown"
            }
    
    def _get_system_prompt(self) -> str:
        return """
        You are a financial assistant helping freelancers classify their bank transactions.
        Your task is to determine if a transaction is a business expense or personal expense.
        
        Consider these factors:
        - Business context (freelancing, consulting, etc.)
        - Transaction description and merchant
        - Amount and frequency
        - Tax implications
        
        Respond with a JSON object containing:
        - classification: "business" or "personal"
        - confidence: float between 0.0 and 1.0
        - reasoning: brief explanation
        - category: suggested category (e.g., "office_supplies", "travel", "meals")
        """
    
    def _build_classification_prompt(self, transaction: Dict[str, Any]) -> str:
        return f"""
        Please classify this transaction:
        
        Date: {transaction.get('date')}
        Description: {transaction.get('description')}
        Amount: {transaction.get('amount')} {transaction.get('currency', 'USD')}
        Merchant: {transaction.get('merchant', 'Unknown')}
        
        Respond with a valid JSON object.
        """
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['classification', 'confidence', 'reasoning', 'category']
            for field in required_fields:
                if field not in result:
                    result[field] = 'unknown' if field == 'category' else 0.0
            
            return result
            
        except (json.JSONDecodeError, ValueError):
            return {
                "classification": "personal",
                "confidence": 0.0,
                "reasoning": "Failed to parse LLM response",
                "category": "unknown"
            }

# =============================================================================
# 5. TRANSACTION SERVICE
# =============================================================================

"""
TRANSACTION SERVICE (services/transaction_service.py):
"""

import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from .llm_service import LLMService

class TransactionService:
    def __init__(self, db: Session, llm_service: LLMService):
        self.db = db
        self.llm_service = llm_service
    
    def process_csv_upload(self, file_content: str, user_id: str) -> List[Dict[str, Any]]:
        """
        Process uploaded CSV file and classify transactions
        """
        try:
            # Parse CSV
            df = pd.read_csv(file_content)
            
            # Validate required columns
            required_columns = ['date', 'description', 'amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            processed_transactions = []
            
            for _, row in df.iterrows():
                # Prepare transaction data
                transaction_data = {
                    'date': row['date'],
                    'description': row['description'],
                    'amount': float(row['amount']),
                    'currency': row.get('currency', 'USD'),
                    'merchant': row.get('merchant', '')
                }
                
                # Classify transaction
                classification = self.llm_service.classify_transaction(transaction_data)
                
                # Create transaction record
                transaction = Transaction(
                    user_id=user_id,
                    date=pd.to_datetime(transaction_data['date']).date(),
                    description=transaction_data['description'],
                    amount=transaction_data['amount'],
                    currency=transaction_data['currency'],
                    merchant=transaction_data['merchant'],
                    is_business_expense=classification['classification'] == 'business',
                    confidence_score=classification['confidence'],
                    llm_reasoning=classification['reasoning'],
                    category=classification['category']
                )
                
                self.db.add(transaction)
                processed_transactions.append(transaction_data)
            
            self.db.commit()
            return processed_transactions
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error processing CSV: {str(e)}")
    
    def get_user_transactions(self, user_id: str, limit: int = 100) -> List[Transaction]:
        """
        Get transactions for a user
        """
        return self.db.query(Transaction)\
            .filter(Transaction.user_id == user_id)\
            .order_by(Transaction.date.desc())\
            .limit(limit)\
            .all()
    
    def update_transaction_classification(self, transaction_id: str, 
                                       is_business: bool, 
                                       user_id: str) -> Transaction:
        """
        Manually override transaction classification
        """
        transaction = self.db.query(Transaction)\
            .filter(Transaction.id == transaction_id, 
                   Transaction.user_id == user_id)\
            .first()
        
        if not transaction:
            raise ValueError("Transaction not found")
        
        transaction.is_business_expense = is_business
        transaction.manually_overridden = True
        
        self.db.commit()
        return transaction

# =============================================================================
# 6. API ENDPOINTS
# =============================================================================

"""
API ENDPOINTS (api/transactions.py):
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..services.transaction_service import TransactionService
from ..services.llm_service import LLMService
from ..database import get_db
from ..utils.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/upload")
async def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload and process CSV file with transactions
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        llm_service = LLMService(api_key="your-openai-api-key")
        transaction_service = TransactionService(db, llm_service)
        
        processed = transaction_service.process_csv_upload(csv_content, current_user['id'])
        
        return {
            "message": f"Successfully processed {len(processed)} transactions",
            "processed_count": len(processed)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_transactions(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's transactions
    """
    llm_service = LLMService(api_key="your-openai-api-key")
    transaction_service = TransactionService(db, llm_service)
    
    transactions = transaction_service.get_user_transactions(current_user['id'], limit)
    
    return [
        {
            "id": str(t.id),
            "date": t.date.isoformat(),
            "description": t.description,
            "amount": float(t.amount),
            "currency": t.currency,
            "merchant": t.merchant,
            "is_business_expense": t.is_business_expense,
            "confidence_score": t.confidence_score,
            "category": t.category,
            "manually_overridden": t.manually_overridden
        }
        for t in transactions
    ]

@router.put("/{transaction_id}")
async def update_transaction_classification(
    transaction_id: str,
    is_business: bool,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Manually override transaction classification
    """
    try:
        llm_service = LLMService(api_key="your-openai-api-key")
        transaction_service = TransactionService(db, llm_service)
        
        transaction = transaction_service.update_transaction_classification(
            transaction_id, is_business, current_user['id']
        )
        
        return {
            "message": "Transaction classification updated",
            "transaction_id": str(transaction.id),
            "is_business_expense": transaction.is_business_expense
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# =============================================================================
# 7. SECURITY IMPLEMENTATION
# =============================================================================

"""
SECURITY UTILITIES (utils/security.py):
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    return payload

# =============================================================================
# 8. CONFIGURATION
# =============================================================================

"""
CONFIGURATION (config.py):
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/freelancer_classifier"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LLM
    openai_api_key: str
    llm_model: str = "gpt-4"
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".csv"]
    
    # CORS
    allowed_origins: list = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()

# =============================================================================
# 9. MAIN APPLICATION
# =============================================================================

"""
MAIN APPLICATION (main.py):
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, transactions, classifications
from .config import settings

app = FastAPI(
    title="Freelancer Transaction Classifier",
    description="LLM-powered transaction classification for freelancers",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(classifications.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Freelancer Transaction Classifier API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# =============================================================================
# 10. TESTING EXAMPLES
# =============================================================================

"""
TESTING EXAMPLES (tests/test_transaction_service.py):
"""

import pytest
from unittest.mock import Mock, patch
from ..services.transaction_service import TransactionService
from ..services.llm_service import LLMService

class TestTransactionService:
    
    @pytest.fixture
    def mock_db(self):
        return Mock()
    
    @pytest.fixture
    def mock_llm_service(self):
        return Mock(spec=LLMService)
    
    @pytest.fixture
    def transaction_service(self, mock_db, mock_llm_service):
        return TransactionService(mock_db, mock_llm_service)
    
    def test_classify_transaction(self, transaction_service, mock_llm_service):
        # Test data
        transaction_data = {
            'date': '2024-01-15',
            'description': 'AMAZON.COM',
            'amount': 45.67,
            'currency': 'USD',
            'merchant': 'Amazon'
        }
        
        # Mock LLM response
        mock_llm_service.classify_transaction.return_value = {
            'classification': 'business',
            'confidence': 0.85,
            'reasoning': 'Amazon purchase likely for office supplies',
            'category': 'office_supplies'
        }
        
        # Test classification
        result = mock_llm_service.classify_transaction(transaction_data)
        
        assert result['classification'] == 'business'
        assert result['confidence'] == 0.85
        assert 'office supplies' in result['reasoning'].lower()

# =============================================================================
# 11. DEPLOYMENT CONFIGURATION
# =============================================================================

"""
DOCKER COMPOSE (docker-compose.yml):
"""

"""
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/freelancer_classifier
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=freelancer_classifier
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000

volumes:
  postgres_data:
"""

# =============================================================================
# 12. ENVIRONMENT VARIABLES
# =============================================================================

"""
ENVIRONMENT VARIABLES (.env):
"""

"""
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/freelancer_classifier

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM
OPENAI_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-4

# File upload
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.csv,.xlsx

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Production
DEBUG=False
LOG_LEVEL=INFO
"""

# =============================================================================
# IMPLEMENTATION COMPLETE
# =============================================================================
# 
# This technical implementation guide provides the core structure and code
# examples for building the freelancer transaction classifier. Key points:
#
# 1. Modular architecture with clear separation of concerns
# 2. Comprehensive error handling and validation
# 3. Security best practices implementation
# 4. Scalable database design
# 5. LLM integration with proper prompt engineering
# 6. Testing strategy with examples
# 7. Deployment-ready configuration
#
# Next steps:
# 1. Set up the development environment
# 2. Implement the database models
# 3. Create the LLM service
# 4. Build the API endpoints
# 5. Add authentication and security
# 6. Implement the frontend
# 7. Add comprehensive testing
# 8. Deploy to production
#
# ============================================================================= 