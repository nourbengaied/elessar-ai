import pytest
import pandas as pd
from unittest.mock import Mock, patch
from app.services.transaction_service import TransactionService
from app.services.bedrock_service import BedrockService

class TestTransactionService:
    
    @pytest.fixture
    def mock_db(self):
        return Mock()
    
    @pytest.fixture
    def mock_bedrock_service(self):
        return Mock(spec=BedrockService)
    
    @pytest.fixture
    def transaction_service(self, mock_db, mock_bedrock_service):
        return TransactionService(mock_db, mock_bedrock_service)
    
    def test_process_csv_upload_success(self, transaction_service, mock_bedrock_service):
        """Test successful CSV processing"""
        # Mock CSV content
        csv_content = """date,description,amount,currency,merchant
2024-01-15,AMAZON.COM,45.67,USD,Amazon
2024-01-16,STARBUCKS,12.50,USD,Starbucks"""
        
        # Mock Bedrock classification responses
        mock_bedrock_service.classify_transaction.side_effect = [
            {
                'classification': 'business',
                'confidence': 0.85,
                'reasoning': 'Amazon purchase for office supplies',
                'category': 'office_supplies'
            },
            {
                'classification': 'personal',
                'confidence': 0.70,
                'reasoning': 'Coffee purchase',
                'category': 'food_beverages'
            }
        ]
        
        # Mock database operations
        transaction_service.db.add = Mock()
        transaction_service.db.flush = Mock()
        transaction_service.db.commit = Mock()
        
        # Test processing
        result = transaction_service.process_csv_upload(csv_content, "user123")
        
        assert result['processed_count'] == 2
        assert len(result['transactions']) == 2
        assert len(result['errors']) == 0
        assert result['transactions'][0]['classification'] == 'business'
        assert result['transactions'][1]['classification'] == 'personal'
    
    def test_process_csv_upload_missing_columns(self, transaction_service):
        """Test CSV processing with missing columns"""
        # Mock CSV content with missing columns
        csv_content = """date,description
2024-01-15,AMAZON.COM"""
        
        # Test processing
        with pytest.raises(Exception) as exc_info:
            transaction_service.process_csv_upload(csv_content, "user123")
        
        assert "Missing required columns" in str(exc_info.value)
    
    def test_process_csv_upload_invalid_data(self, transaction_service, mock_bedrock_service):
        """Test CSV processing with invalid data"""
        # Mock CSV content with invalid data
        csv_content = """date,description,amount,currency,merchant
2024-01-15,AMAZON.COM,invalid,USD,Amazon"""
        
        # Mock Bedrock service to raise exception
        mock_bedrock_service.classify_transaction.side_effect = Exception("LLM Error")
        
        # Mock database operations
        transaction_service.db.add = Mock()
        transaction_service.db.flush = Mock()
        transaction_service.db.commit = Mock()
        transaction_service.db.rollback = Mock()
        
        # Test processing
        result = transaction_service.process_csv_upload(csv_content, "user123")
        
        assert result['processed_count'] == 0
        assert len(result['errors']) == 1
        assert "Row 1" in result['errors'][0]
    
    def test_get_user_transactions(self, transaction_service):
        """Test getting user transactions"""
        # Mock database query
        mock_transactions = [
            Mock(
                id="trans1",
                date=pd.to_datetime("2024-01-15").date(),
                description="AMAZON.COM",
                amount=45.67,
                currency="USD",
                merchant="Amazon",
                is_business_expense=True,
                confidence_score=0.85,
                category="office_supplies",
                manually_overridden=False,
                llm_reasoning="Amazon purchase for office supplies",
                created_at=pd.to_datetime("2024-01-15")
            )
        ]
        
        transaction_service.db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = mock_transactions
        
        # Test getting transactions
        result = transaction_service.get_user_transactions("user123", 10, 0)
        
        assert len(result) == 1
        assert result[0]['id'] == "trans1"
        assert result[0]['description'] == "AMAZON.COM"
        assert result[0]['is_business_expense'] == True
    
    def test_update_transaction_classification(self, transaction_service):
        """Test updating transaction classification"""
        # Mock transaction
        mock_transaction = Mock(
            id="trans1",
            is_business_expense=False,
            manually_overridden=False
        )
        
        transaction_service.db.query.return_value.filter.return_value.first.return_value = mock_transaction
        transaction_service.db.commit = Mock()
        
        # Test updating classification
        result = transaction_service.update_transaction_classification("trans1", True, "user123")
        
        assert result['id'] == "trans1"
        assert result['is_business_expense'] == True
        assert result['manually_overridden'] == True
        assert "updated successfully" in result['message']
    
    def test_update_transaction_classification_not_found(self, transaction_service):
        """Test updating non-existent transaction"""
        # Mock no transaction found
        transaction_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # Test updating classification
        with pytest.raises(ValueError) as exc_info:
            transaction_service.update_transaction_classification("trans1", True, "user123")
        
        assert "Transaction not found" in str(exc_info.value)
    
    def test_get_transaction_statistics(self, transaction_service):
        """Test getting transaction statistics"""
        # Mock database queries
        transaction_service.db.query.return_value.filter.return_value.count.side_effect = [10, 6, 4, 1]
        
        # Mock average confidence query
        mock_confidence_results = [(0.85,), (0.70,), (0.90,)]
        transaction_service.db.query.return_value.filter.return_value.all.return_value = mock_confidence_results
        
        # Test getting statistics
        result = transaction_service.get_transaction_statistics("user123")
        
        assert result['total_transactions'] == 10
        assert result['business_transactions'] == 6
        assert result['personal_transactions'] == 4
        assert result['overridden_transactions'] == 1
        assert result['average_confidence'] == 0.82  # (0.85 + 0.70 + 0.90) / 3
        assert result['business_percentage'] == 60.0  # (6 / 10) * 100 