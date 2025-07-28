import boto3
import json
from typing import Dict, Any
from ..config import settings

class BedrockService:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.model_id = settings.bedrock_model_id
    
    def classify_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a transaction using AWS Bedrock Claude
        """
        prompt = self._build_classification_prompt(transaction_data)
        
        try:
            # Prepare the request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Make the API call
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            result = self._parse_llm_response(content)
            return result
            
        except Exception as e:
            return {
                "classification": "personal",
                "confidence": 0.0,
                "reasoning": f"Error in classification: {str(e)}",
                "category": "unknown"
            }
    
    def _build_classification_prompt(self, transaction: Dict[str, Any]) -> str:
        system_prompt = """You are a financial assistant helping freelancers classify their bank transactions.
Your task is to determine if a transaction is a business expense or personal expense.

Consider these factors:
- Business context (freelancing, consulting, etc.)
- Transaction description and merchant
- Amount and frequency
- Tax implications

Respond with a JSON object containing:
- classification: "business" or "personal"
- confidence: float between 0.0 and 1.0
- reasoning: brief explanation
- category: suggested category (e.g., "office_supplies", "travel", "meals")"""

        user_prompt = f"""Please classify this transaction:

Date: {transaction.get('date')}
Description: {transaction.get('description')}
Amount: {transaction.get('amount')} {transaction.get('currency', 'USD')}
Merchant: {transaction.get('merchant', 'Unknown')}

Respond with a valid JSON object."""

        return f"{system_prompt}\n\n{user_prompt}"
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['classification', 'confidence', 'reasoning', 'category']
            for field in required_fields:
                if field not in result:
                    result[field] = 'unknown' if field == 'category' else 0.0
            
            # Ensure classification is valid
            if result['classification'] not in ['business', 'personal']:
                result['classification'] = 'personal'
            
            # Ensure confidence is between 0 and 1
            result['confidence'] = max(0.0, min(1.0, float(result['confidence'])))
            
            return result
            
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            return {
                "classification": "personal",
                "confidence": 0.0,
                "reasoning": f"Failed to parse LLM response: {str(e)}",
                "category": "unknown"
            }
    
    def batch_classify_transactions(self, transactions: list) -> list:
        """
        Classify multiple transactions (for future optimization)
        """
        results = []
        for transaction in transactions:
            result = self.classify_transaction(transaction)
            results.append(result)
        return results 