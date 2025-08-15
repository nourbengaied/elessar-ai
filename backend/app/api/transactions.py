from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import io
import logging
from datetime import datetime
from pydantic import BaseModel
from ..database import get_db
from ..services.bedrock_service import BedrockService
from ..services.transaction_service import TransactionService
from ..utils.security import get_current_user
from ..utils.validators import validate_file_size, validate_file_type
from ..config import settings
import os

# Configure logging
logger = logging.getLogger(__name__)

# Request models
class UpdateClassificationRequest(BaseModel):
    is_business: bool

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/upload")
async def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload and process CSV or PDF file with transactions
    """
    upload_id = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{current_user['sub'][:8]}"
    
    logger.info(f"[{upload_id}] Starting file upload - User: {current_user['sub']}, File: {file.filename}, Size: {file.size} bytes")
    
    # Check for cancellation before starting
    cancellation_key = f"cancel_{current_user['sub']}"
    cancellation_file = f"/tmp/{cancellation_key}"
    
    try:
        # Validate file type
        logger.info(f"[{upload_id}] Validating file type: {file.filename}")
        if not validate_file_type(file.filename, settings.allowed_file_types):
            logger.warning(f"[{upload_id}] File type validation failed - File: {file.filename}, Allowed: {settings.allowed_file_types}")
            raise HTTPException(
                status_code=400, 
                detail=f"Only {', '.join(settings.allowed_file_types)} files are supported"
            )
        logger.info(f"[{upload_id}] File type validation passed")
        
        # Validate file size
        logger.info(f"[{upload_id}] Reading file content for size validation")
        content = await file.read()
        logger.info(f"[{upload_id}] File content read - Size: {len(content)} bytes")
        
        if not validate_file_size(len(content), settings.max_file_size):
            logger.warning(f"[{upload_id}] File size validation failed - Size: {len(content)} bytes, Max: {settings.max_file_size} bytes")
            raise HTTPException(
                status_code=400, 
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
            )
        logger.info(f"[{upload_id}] File size validation passed")
        
        # Check for cancellation before processing
        if os.path.exists(cancellation_file):
            logger.info(f"[{upload_id}] Processing cancelled by user request")
            # Clean up cancellation file
            os.remove(cancellation_file)
            raise HTTPException(status_code=499, detail="Processing cancelled by user")
        
        # Initialize services
        logger.info(f"[{upload_id}] Initializing services")
        bedrock_service = BedrockService()
        transaction_service = TransactionService(db, bedrock_service)
        logger.info(f"[{upload_id}] Services initialized successfully")
        
        # Determine file type and process accordingly
        file_extension = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        logger.info(f"[{upload_id}] Processing file with extension: {file_extension}")
        
        start_time = datetime.now()
        
        if file_extension == 'csv':
            # Process CSV file
            logger.info(f"[{upload_id}] Processing CSV file")
            csv_content = content.decode('utf-8')
            logger.info(f"[{upload_id}] CSV content decoded - Length: {len(csv_content)} characters")
            
            # Check for cancellation before CSV processing
            if os.path.exists(cancellation_file):
                logger.info(f"[{upload_id}] Processing cancelled before CSV processing")
                os.remove(cancellation_file)
                raise HTTPException(status_code=499, detail="Processing cancelled by user")
            
            result = transaction_service.process_csv_upload(csv_content, current_user["sub"])
            logger.info(f"[{upload_id}] CSV processing completed - Result: {result}")
        elif file_extension == 'pdf':
            # Process PDF file
            logger.info(f"[{upload_id}] Processing PDF file")
            
            # Check for cancellation before PDF processing
            if os.path.exists(cancellation_file):
                logger.info(f"[{upload_id}] Processing cancelled before PDF processing")
                os.remove(cancellation_file)
                raise HTTPException(status_code=499, detail="Processing cancelled by user")
            
            result = transaction_service.process_pdf_upload(content, current_user["sub"])
            logger.info(f"[{upload_id}] PDF processing completed - Result: {result}")
        else:
            logger.error(f"[{upload_id}] Unsupported file type: {file_extension}")
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Final cancellation check
        if os.path.exists(cancellation_file):
            logger.info(f"[{upload_id}] Processing cancelled after completion")
            os.remove(cancellation_file)
            raise HTTPException(status_code=499, detail="Processing cancelled by user")
        
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"[{upload_id}] File processing completed successfully - Processing time: {processing_time:.2f}s, Transactions processed: {result.get('processed_count', 0)}")
        
        return {
            "message": f"Successfully processed {result['processed_count']} transactions",
            "processed_count": result['processed_count'],
            "errors": result['errors'],
            "transactions": result['transactions'],
            "upload_id": upload_id,
            "processing_time": processing_time
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions without logging (they're expected)
        raise
    except Exception as e:
        logger.error(f"[{upload_id}] Unexpected error during file upload: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        # Clean up cancellation file if it exists
        if os.path.exists(cancellation_file):
            os.remove(cancellation_file)

@router.get("/")
async def get_transactions(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's transactions with pagination
    """
    try:
        bedrock_service = BedrockService()
        transaction_service = TransactionService(db, bedrock_service)
        
        transactions = transaction_service.get_user_transactions(
            current_user["sub"], limit, offset
        )
        
        return {
            "transactions": transactions,
            "limit": limit,
            "offset": offset,
            "count": len(transactions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific transaction by ID
    """
    try:
        bedrock_service = BedrockService()
        transaction_service = TransactionService(db, bedrock_service)
        
        transaction = transaction_service.get_transaction_by_id(
            transaction_id, current_user["sub"]
        )
        
        return transaction
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{transaction_id}")
async def update_transaction_classification(
    transaction_id: str,
    request: UpdateClassificationRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Manually override transaction classification
    """
    try:
        bedrock_service = BedrockService()
        transaction_service = TransactionService(db, bedrock_service)
        
        result = transaction_service.update_transaction_classification(
            transaction_id, request.is_business, current_user["sub"]
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a transaction
    """
    try:
        from ..models.transaction import Transaction
        
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user["sub"]
        ).first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        db.delete(transaction)
        db.commit()
        
        return {"message": "Transaction deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
async def clear_all_transactions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Clear all transactions for the current user
    """
    try:
        from ..models.transaction import Transaction
        from ..models.classification import Classification
        
        # Get count before deletion for logging
        transaction_count = db.query(Transaction).filter(
            Transaction.user_id == current_user["sub"]
        ).count()
        
        # Delete all transactions for the user
        # Note: Classifications will be deleted via cascade
        deleted_transactions = db.query(Transaction).filter(
            Transaction.user_id == current_user["sub"]
        ).delete()
        
        db.commit()
        
        logger.info(f"Cleared {deleted_transactions} transactions for user {current_user['sub']}")
        
        return {
            "message": f"Successfully cleared {deleted_transactions} transactions",
            "deleted_count": deleted_transactions
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error clearing transactions for user {current_user['sub']}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cancel-processing")
async def cancel_transaction_processing(
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel ongoing transaction processing for the current user
    """
    try:
        # Store cancellation request in a simple way (in production, you might use Redis or a database)
        # For now, we'll use a simple file-based approach or in-memory storage
        cancellation_key = f"cancel_{current_user['sub']}"
        
        # In a real implementation, you'd store this in Redis or a database
        # For now, we'll create a simple cancellation marker
        import os
        cancellation_file = f"/tmp/{cancellation_key}"
        
        with open(cancellation_file, 'w') as f:
            f.write(str(datetime.now().isoformat()))
        
        logger.info(f"Processing cancellation requested for user {current_user['sub']}")
        
        return {
            "message": "Processing cancellation requested",
            "cancellation_key": cancellation_key
        }
        
    except Exception as e:
        logger.error(f"Error requesting processing cancellation for user {current_user['sub']}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics/summary")
async def get_transaction_statistics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get transaction statistics for the user
    """
    try:
        bedrock_service = BedrockService()
        transaction_service = TransactionService(db, bedrock_service)
        
        stats = transaction_service.get_transaction_statistics(current_user["sub"])
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 