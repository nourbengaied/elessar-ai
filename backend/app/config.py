from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/freelancer_classifier"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AWS Bedrock
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".csv"]
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # Application
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        # env_file = ".env"
        env_file = str(Path(__file__).resolve().parents[2] / ".env")


settings = Settings() 