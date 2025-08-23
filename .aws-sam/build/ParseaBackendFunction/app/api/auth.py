from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..services.user_service import UserService
from ..utils.security import create_access_token, get_current_user
from ..utils.validators import validate_email, validate_password
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["authentication"])

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    business_name: Optional[str] = None
    business_type: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str

class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    created_at: str

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister):
    """
    Register a new user
    """
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")
        
        # Validate email
        logger.info("Validating email...")
        if not validate_email(user_data.email):
            logger.warning(f"Invalid email format: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate password
        logger.info("Validating password...")
        if not validate_password(user_data.password):
            logger.warning("Password validation failed")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
        
        # Create user service
        logger.info("Creating user service...")
        user_service = UserService()
        
        # Create user
        logger.info("Creating user in database...")
        user = user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            business_name=user_data.business_name,
            business_type=user_data.business_type
        )
        
        logger.info("User created, generating token...")
        # Create access token
        access_token = create_access_token(data={"sub": user["email"], "user_id": user["id"]})
        
        logger.info(f"User registered successfully: {user_data.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user["id"],
            email=user["email"]
        )
        
    except ValueError as e:
        logger.warning(f"Registration validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """
    Login user and return access token
    """
    try:
        # Create user service
        user_service = UserService()
        
        # Authenticate user
        user = user_service.authenticate_user(user_data.email, user_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user["email"], "user_id": user["id"]})
        
        logger.info(f"User logged in successfully: {user_data.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user["id"],
            email=user["email"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile
    """
    try:
        return UserProfile(
            id=current_user["id"],
            email=current_user["email"],
            full_name=current_user.get("full_name", ""),
            business_name=current_user.get("business_name"),
            business_type=current_user.get("business_type"),
            created_at=current_user.get("created_at", "")
        )
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information (simple endpoint)
    """
    return {
        "user_id": current_user["id"],
        "email": current_user["email"],
        "full_name": current_user.get("full_name", ""),
        "business_name": current_user.get("business_name", "")
    } 