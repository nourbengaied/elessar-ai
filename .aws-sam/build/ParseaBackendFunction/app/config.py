import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Security - Use JWT_SECRET from environment
    secret_key: str = os.getenv("JWT_SECRET", "fallback-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AWS - Use environment variables (available in Lambda)
    aws_region: str = os.getenv("AWS_REGION", "eu-west-2")
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # DynamoDB
    dynamodb_table: str = os.getenv("DYNAMODB_TABLE", "parsea-transactions")
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".csv", ".pdf"]
    
    # CORS
    allowed_origins: List[str] = ["*"]  # Allow all origins for now
    
    # Application
    debug: bool = False
    log_level: str = "INFO"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        # Don't require .env file in Lambda
        env_file = None


settings = Settings() 