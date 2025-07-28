import pytest
from unittest.mock import Mock, patch
from app.services.bedrock_service import BedrockService

class TestBedrockService:
    
    @pytest.fixture
    def bedrock_service(self):
        with patch('boto3.client'):
            service = BedrockService()
            service.client = Mock()
            return service
    
    def test_classify_transaction_success(self, bedrock_service):
        """Test successful transaction classification"""
        # Mock response
        mock_response = {
            'body': Mock(
                read=lambda: b'{"content": [{"text": \'{"classification": "business", "confidence": 0.85, "reasoning": "Amazon purchase for office supplies", "category": "office_supplies"}\'}]}'
            )
        }
        bedrock_service.client.invoke_model.return_value = mock_response
        
        # Test data
        transaction_data = {
            'date': '2024-01-15',
            'description': 'AMAZON.COM',
            'amount': 45.67,
            'currency': 'USD',
            'merchant': 'Amazon'
        }
        
        # Test classification
        result = bedrock_service.classify_transaction(transaction_data)
        
        assert result['classification'] == 'business'
        assert result['confidence'] == 0.85
        assert 'office supplies' in result['reasoning'].lower()
        assert result['category'] == 'office_supplies'
    
    def test_classify_transaction_error_handling(self, bedrock_service):
        """Test error handling in classification"""
        # Mock error response
        bedrock_service.client.invoke_model.side_effect = Exception("API Error")
        
        # Test data
        transaction_data = {
            'date': '2024-01-15',
            'description': 'AMAZON.COM',
            'amount': 45.67,
            'currency': 'USD',
            'merchant': 'Amazon'
        }
        
        # Test classification with error
        result = bedrock_service.classify_transaction(transaction_data)
        
        assert result['classification'] == 'personal'
        assert result['confidence'] == 0.0
        assert 'Error in classification' in result['reasoning']
        assert result['category'] == 'unknown'
    
    def test_parse_llm_response_invalid_json(self, bedrock_service):
        """Test parsing invalid JSON response"""
        # Mock response with invalid JSON
        mock_response = {
            'body': Mock(
                read=lambda: b'{"content": [{"text": "Invalid JSON response"}]}'
            )
        }
        bedrock_service.client.invoke_model.return_value = mock_response
        
        # Test data
        transaction_data = {
            'date': '2024-01-15',
            'description': 'AMAZON.COM',
            'amount': 45.67,
            'currency': 'USD',
            'merchant': 'Amazon'
        }
        
        # Test classification
        result = bedrock_service.classify_transaction(transaction_data)
        
        assert result['classification'] == 'personal'
        assert result['confidence'] == 0.0
        assert 'Failed to parse LLM response' in result['reasoning']
        assert result['category'] == 'unknown'
    
    def test_parse_llm_response_missing_fields(self, bedrock_service):
        """Test parsing response with missing fields"""
        # Mock response with missing fields
        mock_response = {
            'body': Mock(
                read=lambda: b'{"content": [{"text": \'{"classification": "business"}\'}]}'
            )
        }
        bedrock_service.client.invoke_model.return_value = mock_response
        
        # Test data
        transaction_data = {
            'date': '2024-01-15',
            'description': 'AMAZON.COM',
            'amount': 45.67,
            'currency': 'USD',
            'merchant': 'Amazon'
        }
        
        # Test classification
        result = bedrock_service.classify_transaction(transaction_data)
        
        assert result['classification'] == 'business'
        assert result['confidence'] == 0.0  # Default value
        assert result['category'] == 'unknown'  # Default value
    
    def test_build_classification_prompt(self, bedrock_service):
        """Test prompt building"""
        transaction_data = {
            'date': '2024-01-15',
            'description': 'AMAZON.COM',
            'amount': 45.67,
            'currency': 'USD',
            'merchant': 'Amazon'
        }
        
        prompt = bedrock_service._build_classification_prompt(transaction_data)
        
        assert '2024-01-15' in prompt
        assert 'AMAZON.COM' in prompt
        assert '45.67' in prompt
        assert 'USD' in prompt
        assert 'Amazon' in prompt
        assert 'JSON' in prompt 