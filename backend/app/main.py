from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from .api import auth_router, transactions_router, export_router
from .config import settings
from .database import engine, Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

# Set specific log levels for different modules
logging.getLogger('uvicorn').setLevel(logging.INFO)
logging.getLogger('uvicorn.access').setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Starting Freelancer Transaction Classifier API")

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created/verified")

# Create FastAPI app
app = FastAPI(
    title="Freelancer Transaction Classifier",
    description="LLM-powered transaction classification for freelancers using AWS Bedrock",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured")

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")
app.include_router(export_router, prefix="/api/v1")

logger.info("API routers included")

@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Freelancer Transaction Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy", "service": "transaction-classifier"}

@app.get("/info")
async def info():
    """API information"""
    logger.info("Info endpoint accessed")
    return {
        "name": "Freelancer Transaction Classifier",
        "description": "LLM-powered transaction classification using AWS Bedrock",
        "version": "1.0.0",
        "features": [
            "CSV transaction upload",
            "PDF bank statement processing",
            "AWS Bedrock LLM classification",
            "Manual override capabilities",
            "Export functionality",
            "Tax report generation"
        ]
    }

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("🚀 Application starting up...")
    logger.info(f"📊 Database URL: {settings.database_url}")
    logger.info(f"🌐 Allowed origins: {settings.allowed_origins}")
    logger.info(f"📁 Max file size: {settings.max_file_size} bytes")
    logger.info(f"📄 Allowed file types: {settings.allowed_file_types}")
    logger.info("✅ Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("🛑 Application shutting down...") 