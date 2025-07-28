from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..services.bedrock_service import BedrockService
from ..services.transaction_service import TransactionService
from ..utils.security import get_current_user
from ..utils.validators import validate_file_size, validate_file_type
from ..config import settings

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
    # Validate file type
    if not validate_file_type(file.filename, settings.allowed_file_types):
        raise HTTPException(
            status_code=400, 
            detail=f"Only {', '.join(settings.allowed_file_types)} files are supported"
        )
    
    # Validate file size
    content = await file.read()
    if not validate_file_size(len(content), settings.max_file_size):
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
        )
    
    try:
        csv_content = content.decode('utf-8')
        
        # Initialize services
        bedrock_service = BedrockService()
        transaction_service = TransactionService(db, bedrock_service)
        
        # Process CSV
        result = transaction_service.process_csv_upload(csv_content, current_user["sub"])
        
        return {
            "message": f"Successfully processed {result['processed_count']} transactions",
            "processed_count": result['processed_count'],
            "errors": result['errors'],
            "transactions": result['transactions']
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    is_business: bool,
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
            transaction_id, is_business, current_user["sub"]
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