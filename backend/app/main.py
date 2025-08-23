from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os
from .api import auth_router  # , transactions_router, export_router
from .config import settings
from .database import get_dynamodb_table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific log levels for different modules
logging.getLogger('uvicorn').setLevel(logging.INFO)
logging.getLogger('uvicorn.access').setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Starting Parsea Transaction Classifier API")

# Verify DynamoDB table connection
try:
    table = get_dynamodb_table()
    logger.info(f"DynamoDB table verified: {table.table_name}")
except Exception as e:
    logger.error(f"DynamoDB table connection failed: {e}")

# Create FastAPI app
app = FastAPI(
    title="Parsea - Transaction Classifier",
    description="AI-powered transaction classification for freelancers using AWS Bedrock",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured")

# Include routers
app.include_router(auth_router, prefix="/auth")
# TODO: Convert transactions to DynamoDB before re-enabling
# app.include_router(transactions_router, prefix="/transactions")
# app.include_router(export_router, prefix="/export")

logger.info("API routers included")

@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Parsea Transaction Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check accessed")
    try:
        # Test DynamoDB connection
        table = get_dynamodb_table()
        table_status = table.table_status
        
        return {
            "status": "healthy",
            "database": "connected",
            "table_status": table_status,
            "environment": os.getenv("ENVIRONMENT", "unknown")
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)}
    )

# Temporary stub endpoints for transactions (until DynamoDB conversion is complete)
@app.get("/transactions/statistics/summary")
async def get_transaction_statistics_stub():
    """Temporary stub for transaction statistics"""
    return {
        "total_transactions": 0,
        "business_expenses": 0.0,
        "personal_expenses": 0.0,
        "business_income": 0.0,
        "personal_income": 0.0,
        "categories": {}
    }

@app.get("/transactions/")
async def get_transactions_stub():
    """Temporary stub for transactions list"""
    return {
        "transactions": [],
        "limit": 100,
        "offset": 0,
        "count": 0
    }

@app.delete("/transactions/")
async def clear_transactions_stub():
    """Temporary stub for clearing transactions"""
    return {
        "message": "No transactions to clear (transactions API not yet implemented)",
        "deleted_count": 0
    }

@app.post("/transactions/upload")
async def upload_transactions_stub():
    """Temporary stub for transaction upload"""
    return {
        "message": "Upload feature not yet implemented - transactions API being converted to DynamoDB",
        "processed_count": 0,
        "errors": [],
        "transactions": []
    } 