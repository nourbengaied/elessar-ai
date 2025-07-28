import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..models.classification import Classification
from .bedrock_service import BedrockService
from datetime import datetime

class TransactionService:
    def __init__(self, db: Session, bedrock_service: BedrockService):
        self.db = db
        self.bedrock_service = bedrock_service
    
    def process_csv_upload(self, file_content: str, user_id: str) -> Dict[str, Any]:
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
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Prepare transaction data
                    transaction_data = {
                        'date': row['date'],
                        'description': row['description'],
                        'amount': float(row['amount']),
                        'currency': row.get('currency', 'USD'),
                        'merchant': row.get('merchant', '')
                    }
                    
                    # Classify transaction using Bedrock
                    classification = self.bedrock_service.classify_transaction(transaction_data)
                    
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
                    self.db.flush()  # Get the transaction ID
                    
                    # Create classification record
                    classification_record = Classification(
                        transaction_id=transaction.id,
                        classification_type=classification['classification'],
                        confidence_score=classification['confidence'],
                        llm_reasoning=classification['reasoning'],
                        user_override=False
                    )
                    
                    self.db.add(classification_record)
                    processed_transactions.append({
                        'id': str(transaction.id),
                        'date': transaction_data['date'],
                        'description': transaction_data['description'],
                        'amount': transaction_data['amount'],
                        'classification': classification['classification'],
                        'confidence': classification['confidence'],
                        'category': classification['category']
                    })
                    
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
                    continue
            
            self.db.commit()
            
            return {
                "processed_count": len(processed_transactions),
                "transactions": processed_transactions,
                "errors": errors
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error processing CSV: {str(e)}")
    
    def get_user_transactions(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get transactions for a user with pagination
        """
        transactions = self.db.query(Transaction)\
            .filter(Transaction.user_id == user_id)\
            .order_by(Transaction.date.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
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
                "manually_overridden": t.manually_overridden,
                "llm_reasoning": t.llm_reasoning,
                "created_at": t.created_at.isoformat()
            }
            for t in transactions
        ]
    
    def get_transaction_by_id(self, transaction_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get a specific transaction by ID
        """
        transaction = self.db.query(Transaction)\
            .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)\
            .first()
        
        if not transaction:
            raise ValueError("Transaction not found")
        
        return {
            "id": str(transaction.id),
            "date": transaction.date.isoformat(),
            "description": transaction.description,
            "amount": float(transaction.amount),
            "currency": transaction.currency,
            "merchant": transaction.merchant,
            "is_business_expense": transaction.is_business_expense,
            "confidence_score": transaction.confidence_score,
            "category": transaction.category,
            "manually_overridden": transaction.manually_overridden,
            "llm_reasoning": transaction.llm_reasoning,
            "created_at": transaction.created_at.isoformat()
        }
    
    def update_transaction_classification(self, transaction_id: str, 
                                       is_business: bool, 
                                       user_id: str) -> Dict[str, Any]:
        """
        Manually override transaction classification
        """
        transaction = self.db.query(Transaction)\
            .filter(Transaction.id == transaction_id, 
                   Transaction.user_id == user_id)\
            .first()
        
        if not transaction:
            raise ValueError("Transaction not found")
        
        # Update transaction
        transaction.is_business_expense = is_business
        transaction.manually_overridden = True
        transaction.updated_at = datetime.utcnow()
        
        # Create new classification record for the override
        classification = Classification(
            transaction_id=transaction.id,
            classification_type="business" if is_business else "personal",
            confidence_score=1.0,  # User override has full confidence
            llm_reasoning="Manually overridden by user",
            user_override=True
        )
        
        self.db.add(classification)
        self.db.commit()
        
        return {
            "id": str(transaction.id),
            "is_business_expense": transaction.is_business_expense,
            "manually_overridden": transaction.manually_overridden,
            "message": "Transaction classification updated successfully"
        }
    
    def get_transaction_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics for user's transactions
        """
        total_transactions = self.db.query(Transaction)\
            .filter(Transaction.user_id == user_id)\
            .count()
        
        business_transactions = self.db.query(Transaction)\
            .filter(Transaction.user_id == user_id, Transaction.is_business_expense == True)\
            .count()
        
        personal_transactions = self.db.query(Transaction)\
            .filter(Transaction.user_id == user_id, Transaction.is_business_expense == False)\
            .count()
        
        overridden_transactions = self.db.query(Transaction)\
            .filter(Transaction.user_id == user_id, Transaction.manually_overridden == True)\
            .count()
        
        avg_confidence = self.db.query(Transaction.confidence_score)\
            .filter(Transaction.user_id == user_id)\
            .all()
        
        avg_confidence = sum([t[0] for t in avg_confidence if t[0] is not None]) / len(avg_confidence) if avg_confidence else 0
        
        return {
            "total_transactions": total_transactions,
            "business_transactions": business_transactions,
            "personal_transactions": personal_transactions,
            "overridden_transactions": overridden_transactions,
            "average_confidence": round(avg_confidence, 2),
            "business_percentage": round((business_transactions / total_transactions * 100) if total_transactions > 0 else 0, 2)
        } 