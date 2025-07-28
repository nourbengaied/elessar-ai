from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth_router, transactions_router, export_router
from .config import settings
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")
app.include_router(export_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Freelancer Transaction Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "transaction-classifier"}

@app.get("/info")
async def info():
    """API information"""
    return {
        "name": "Freelancer Transaction Classifier",
        "description": "LLM-powered transaction classification using AWS Bedrock",
        "version": "1.0.0",
        "features": [
            "CSV transaction upload",
            "AWS Bedrock LLM classification",
            "Manual override capabilities",
            "Export functionality",
            "Tax report generation"
        ]
    } 