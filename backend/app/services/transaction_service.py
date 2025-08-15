import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..models.classification import Classification
from .bedrock_service import BedrockService
from datetime import datetime
import PyPDF2
import io
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, db: Session, bedrock_service: BedrockService):
        self.db = db
        self.bedrock_service = bedrock_service
    
    def _check_cancellation(self, user_id: str) -> bool:
        """Check if processing has been cancelled for the user"""
        cancellation_file = f"/tmp/cancel_{user_id}"
        return os.path.exists(cancellation_file)
    
    def process_csv_upload(self, file_content: str, user_id: str) -> Dict[str, Any]:
        """
        Process uploaded CSV file and classify transactions
        """
        logger.info(f"Starting CSV processing for user {user_id}")
        start_time = datetime.now()
        
        try:
            # Parse CSV
            logger.info("Parsing CSV content with pandas")
            df = pd.read_csv(file_content)
            logger.info(f"CSV parsed successfully - Rows: {len(df)}, Columns: {list(df.columns)}")
            
            # Validate required columns
            required_columns = ['date', 'description', 'amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            logger.info("Column validation passed")
            processed_transactions = []
            errors = []
            
            logger.info(f"Processing {len(df)} rows of transaction data")
            for index, row in df.iterrows():
                # Check for cancellation on every row for instant response
                if self._check_cancellation(user_id):
                    logger.info(f"Processing cancelled at row {index + 1}")
                    raise ValueError("Processing cancelled by user")
                
                try:
                    logger.debug(f"Processing row {index + 1}: {row.to_dict()}")
                    
                    # Prepare transaction data
                    transaction_data = {
                        'date': row['date'],
                        'description': row['description'],
                        'amount': float(row['amount']),
                        'currency': row.get('currency', 'USD'),
                        'merchant': row.get('merchant', '')
                    }
                    
                    logger.debug(f"Transaction data prepared: {transaction_data}")
                    
                    # Check for cancellation before Bedrock API call (most time-consuming operation)
                    if self._check_cancellation(user_id):
                        logger.info(f"Processing cancelled before Bedrock classification at row {index + 1}")
                        raise ValueError("Processing cancelled by user")
                    
                    # Classify transaction using Bedrock
                    logger.debug(f"Classifying transaction {index + 1} with Bedrock")
                    classification = self.bedrock_service.classify_transaction(transaction_data, user_id)
                    logger.debug(f"Classification result: {classification}")
                    
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
                    logger.debug(f"Transaction record created with ID: {transaction.id}")
                    
                    # Create classification record
                    classification_record = Classification(
                        transaction_id=transaction.id,
                        classification_type=classification['classification'],
                        confidence_score=classification['confidence'],
                        llm_reasoning=classification['reasoning'],
                        user_override=False
                    )
                    
                    self.db.add(classification_record)
                    logger.debug(f"Classification record created for transaction {transaction.id}")
                    
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
                    error_msg = f"Row {index + 1}: {str(e)}"
                    logger.error(f"Error processing row {index + 1}: {str(e)}")
                    errors.append(error_msg)
                    continue
            
            self.db.commit()
            processing_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"CSV processing completed successfully - Processed: {len(processed_transactions)}, Errors: {len(errors)}, Time: {processing_time:.2f}s")
            
            return {
                "processed_count": len(processed_transactions),
                "transactions": processed_transactions,
                "errors": errors,
                "processing_time": processing_time
            }
            
        except Exception as e:
            self.db.rollback()
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"CSV processing failed after {processing_time:.2f}s: {str(e)}", exc_info=True)
            raise Exception(f"Error processing CSV: {str(e)}")
    
    def process_pdf_upload(self, file_content: bytes, user_id: str) -> Dict[str, Any]:
        """
        Process uploaded PDF bank statement and extract/classify transactions
        """
        logger.info(f"Starting PDF processing for user {user_id}")
        start_time = datetime.now()
        
        try:
            logger.info("Extracting text from PDF")
            # extract text from pdf
            pdf_text = self._extract_text_from_pdf(file_content)
            logger.info(f"PDF text extracted - Length: {len(pdf_text)} characters")
            
            logger.info("Extracting transactions from PDF text using Bedrock")
            # extract transactions from pdf text
            extracted_transactions = self.bedrock_service.extract_transactions_from_pdf(pdf_text, user_id)
            logger.info(f"Transactions extracted from PDF: {len(extracted_transactions)} found")
            
            processed_transactions = []
            errors = []
            
            logger.info("Processing extracted transactions")
            for index, transaction_data in enumerate(extracted_transactions):
                # Check for cancellation on every transaction for instant response
                if self._check_cancellation(user_id):
                    logger.info(f"Processing cancelled at transaction {index + 1}")
                    raise ValueError("Processing cancelled by user")
                
                try:
                    logger.debug(f"Processing extracted transaction {index + 1}: {transaction_data}")
                    
                    # Validate required fields
                    if not all(key in transaction_data for key in ['date', 'description', 'amount']):
                        missing = [key for key in ['date', 'description', 'amount'] if key not in transaction_data]
                        logger.warning(f"Transaction {index + 1} missing required fields: {missing}")
                        errors.append(f"Transaction {index + 1}: Missing required fields {missing}")
                        continue
                    
                    # Check for cancellation before Bedrock API call (most time-consuming operation)
                    if self._check_cancellation(user_id):
                        logger.info(f"Processing cancelled before Bedrock classification at transaction {index + 1}")
                        raise ValueError("Processing cancelled by user")
                    
                    # Classify transaction using Bedrock
                    logger.debug(f"Classifying extracted transaction {index + 1}")
                    classification = self.bedrock_service.classify_transaction(transaction_data, user_id)
                    logger.debug(f"Classification result: {classification}")
                    
                    # Create transaction record
                    transaction = Transaction(
                        user_id=user_id,
                        date=pd.to_datetime(transaction_data['date']).date(),
                        description=transaction_data['description'],
                        amount=float(transaction_data['amount']),
                        currency=transaction_data.get('currency', 'USD'),
                        merchant=transaction_data.get('merchant', ''),
                        is_business_expense=classification['classification'] == 'business',
                        confidence_score=classification['confidence'],
                        llm_reasoning=classification['reasoning'],
                        category=classification['category']
                    )
                    
                    self.db.add(transaction)
                    self.db.flush()
                    logger.debug(f"Transaction record created with ID: {transaction.id}")
                    
                    # Create classification record
                    classification_record = Classification(
                        transaction_id=transaction.id,
                        classification_type=classification['classification'],
                        confidence_score=classification['confidence'],
                        llm_reasoning=classification['reasoning'],
                        user_override=False
                    )
                    
                    self.db.add(classification_record)
                    logger.debug(f"Classification record created for transaction {transaction.id}")
                    
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
                    error_msg = f"Transaction {index + 1}: {str(e)}"
                    logger.error(f"Error processing extracted transaction {index + 1}: {str(e)}")
                    errors.append(error_msg)
                    continue
            
            self.db.commit()
            processing_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"PDF processing completed successfully - Processed: {len(processed_transactions)}, Errors: {len(errors)}, Time: {processing_time:.2f}s")
            
            return {
                "processed_count": len(processed_transactions),
                "transactions": processed_transactions,
                "errors": errors,
                "processing_time": processing_time
            }
            
        except Exception as e:
            self.db.rollback()
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"PDF processing failed after {processing_time:.2f}s: {str(e)}", exc_info=True)
            raise Exception(f"Error processing PDF: {str(e)}")

    def _extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text content from PDF file
        """
        logger.info("Extracting text from PDF content")
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ""
            
            logger.info(f"PDF has {len(pdf_reader.pages)} pages")
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text_content += page_text + "\n"
                logger.debug(f"Page {page_num + 1} extracted - Length: {len(page_text)} characters")
            
            logger.info(f"PDF text extraction completed - Total length: {len(text_content)} characters")
            return text_content
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}", exc_info=True)
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
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