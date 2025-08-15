import boto3
import json
from typing import Dict, Any, List
import logging
from datetime import datetime
import os
from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)

class BedrockService:
    def __init__(self):
        logger.info("Initializing Bedrock service")
        try:
            self.client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
            self.model_id = settings.bedrock_model_id
            logger.info(f"Bedrock service initialized successfully - Model: {self.model_id}, Region: {settings.aws_region}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock service: {str(e)}", exc_info=True)
            raise
    
    def _check_cancellation(self, user_id: str) -> bool:
        """Check if processing has been cancelled for the user"""
        cancellation_file = f"/tmp/cancel_{user_id}"
        return os.path.exists(cancellation_file)
    
    def classify_transaction(self, transaction_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """
        Classify a transaction using AWS Bedrock Claude
        """
        request_id = f"classify_{datetime.now().strftime('%H%M%S%f')[:-3]}"
        # logger.info(f"[{request_id}] Starting transaction classification - Data: {transaction_data}")
        start_time = datetime.now()
        
        # Check for cancellation before starting classification
        if user_id and self._check_cancellation(user_id):
            logger.info(f"[{request_id}] Classification cancelled by user request")
            raise ValueError("Processing cancelled by user")
        
        prompt = self._build_classification_prompt(transaction_data)
        logger.debug(f"[{request_id}] Classification prompt built - Length: {len(prompt)} characters")
        logger.debug(f"[{request_id}] Full classification prompt:\n{prompt}")
        
        try:
            # Prepare the request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096, 
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            logger.debug(f"[{request_id}] Making Bedrock API call to model {self.model_id}")
            logger.debug(f"[{request_id}] Request body: {json.dumps(request_body, indent=2)}")
            
            # Make the API call
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            logger.debug(f"[{request_id}] Bedrock API response received")
            logger.debug(f"[{request_id}] Raw Bedrock response: {response}")
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            logger.info(f"[{request_id}] Raw Bedrock text response:\n{content}")
            logger.debug(f"[{request_id}] Response content: {content}")
            
            result = self._parse_llm_response(content)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # logger.info(f"[{request_id}] Classification completed successfully - Result: {result}, Time: {processing_time:.3f}s")
            # logger.info(f"[{request_id}] Parsed result: {json.dumps(result, indent=2)}")
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"[{request_id}] Classification failed after {processing_time:.3f}s: {str(e)}", exc_info=True)
            return {
                "classification": "personal",
                "confidence": 0.0,
                "reasoning": f"Error in classification: {str(e)}",
                "category": "unknown"
            }
    
    def extract_transactions_from_pdf(self, pdf_text: str, user_id: str = None) -> List[Dict[str, Any]]:
        """
        Extract transactions from PDF bank statement text using AWS Bedrock Claude
        """
        request_id = f"extract_{datetime.now().strftime('%H%M%S%f')[:-3]}"
        logger.info(f"[{request_id}] Starting PDF transaction extraction - Text length: {len(pdf_text)} characters")
        start_time = datetime.now()
        
        # Check for cancellation before starting extraction
        if user_id and self._check_cancellation(user_id):
            logger.info(f"[{request_id}] PDF extraction cancelled by user request")
            raise ValueError("Processing cancelled by user")
        
        prompt = self._build_pdf_extraction_prompt(pdf_text)
        logger.debug(f"[{request_id}] PDF extraction prompt built - Length: {len(prompt)} characters")
        logger.debug(f"[{request_id}] Full PDF extraction prompt:\n{prompt}")
        
        try:
            # Prepare the request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096, 
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            logger.debug(f"[{request_id}] Making Bedrock API call to model {self.model_id}")
            logger.debug(f"[{request_id}] Request body: {json.dumps(request_body, indent=2)}")
            
            # Make the API call
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            logger.debug(f"[{request_id}] Bedrock API response received")
            logger.debug(f"[{request_id}] Raw Bedrock response: {response}")
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            logger.info(f"[{request_id}] Raw Bedrock text response:\n{content}")
            logger.debug(f"[{request_id}] Response content: {content}")
            
            result = self._parse_transaction_extraction_response(content)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"[{request_id}] PDF extraction completed successfully - Transactions found: {len(result)}, Time: {processing_time:.3f}s")
            logger.info(f"[{request_id}] Parsed transactions: {json.dumps(result, indent=2)}")
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"[{request_id}] PDF extraction failed after {processing_time:.3f}s: {str(e)}", exc_info=True)
            return []
    
    def _build_classification_prompt(self, transaction: Dict[str, Any]) -> str:
        system_prompt = """You are a financial assistant helping freelancers classify their bank transactions.
Your task is to determine if a transaction is a business expense or personal expense.

CRITICAL INSTRUCTIONS:
1. Return ONLY a simple JSON object
2. Do NOT include any explanatory text before or after the JSON
3. Do NOT create nested structures
4. Use ONLY the exact field names specified

REQUIRED FORMAT:
Return a JSON object with these exact fields:
- classification: "business" or "personal" (string)
- confidence: number between 0.0 and 1.0 (float)
- reasoning: brief explanation as plain text (string)
- category: suggested category as plain text (string)

FEW-SHOT EXAMPLES:

Example 1:
Transaction: Office supplies from Office Depot, $45.50
Correct response: {"classification": "business", "confidence": 0.9, "reasoning": "Office supplies are typically business expenses for freelancers", "category": "office_supplies"}

Example 2:
Transaction: Grocery store purchase, $120.00
Correct response: {"classification": "personal", "confidence": 0.8, "reasoning": "Groceries are personal living expenses", "category": "food_groceries"}

Example 3:
Transaction: Zoom subscription, $1380.44
Correct response: {"classification": "business", "confidence": 0.95, "reasoning": "Video conferencing tools are essential for business communication", "category": "software_subscription"}

Consider these factors when classifying:
- Business context (freelancing, consulting, etc.)
- Transaction description and merchant
- Amount and frequency
- Tax implications"""

        user_prompt = f"""Please classify this transaction:

Date: {transaction.get('date')}
Description: {transaction.get('description')}
Amount: {transaction.get('amount')} {transaction.get('currency', 'USD')}
Merchant: {transaction.get('merchant', 'Unknown')}

Return ONLY a simple JSON object with the required fields. Follow the examples above exactly."""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        logger.debug(f"Classification prompt built:\nSystem: {system_prompt}\n\nUser: {user_prompt}")
        return full_prompt
    
    def _build_pdf_extraction_prompt(self, pdf_text: str) -> str:
        system_prompt = """You are a financial assistant helping freelancers extract transaction data from bank statements.
Your task is to identify and extract individual transactions from the provided bank statement text.

CRITICAL INSTRUCTIONS:
1. Extract ONLY the transaction data, do not create nested structures
2. Each transaction should be a simple, flat JSON object
3. Do NOT put JSON objects inside other fields
4. Use ONLY plain text values for all fields

REQUIRED FORMAT:
Each transaction must be a simple JSON object with these exact fields:
- date: transaction date in YYYY-MM-DD format (e.g., "2024-01-15")
- description: plain text description (e.g., "Zoom Subscription")
- amount: numeric amount as a number, not a string (e.g., -1380.44)
- currency: currency code (e.g., "USD", "GBP", "EUR")
- merchant: merchant name (e.g., "Zoom Video Communications")

FEW-SHOT EXAMPLES:

Example 1 - Bank Statement Line:
"15/01/2024 Zoom Video Communications -1380.44 GBP"
Correct extraction:
{"date": "2024-01-15", "description": "Zoom Video Communications", "amount": -1380.44, "currency": "GBP", "merchant": "Zoom"}

Example 2 - Bank Statement Line:
"16/01/2024 Office Depot Office Supplies -45.50 USD"
Correct extraction:
{"date": "2024-01-16", "description": "Office Supplies", "amount": -45.50, "currency": "USD", "merchant": "Office Depot"}

Example 3 - Bank Statement Line:
"17/01/2024 Client Payment +1500.00 USD"
Correct extraction:
{"date": "2024-01-17", "description": "Client Payment", "amount": 1500.00, "currency": "USD", "merchant": "Client"

Remember: Keep it simple, flat, and clean. No nested objects, no complex structures."""

        user_prompt = f"""Please extract all transactions from this bank statement:

{pdf_text}

Return ONLY a JSON array of simple transaction objects. Each transaction should be flat with no nested structures.
Follow the examples above exactly."""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        logger.debug(f"PDF extraction prompt built:\nSystem: {system_prompt}\n\nUser: {user_prompt}")
        return full_prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        logger.debug(f"Parsing LLM response: {response}")
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("No JSON found in response")
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            logger.debug(f"Extracted JSON string: {json_str}")
            
            result = json.loads(json_str)
            logger.debug(f"Parsed JSON result: {result}")
            
            # Validate required fields
            required_fields = ['classification', 'confidence', 'reasoning', 'category']
            for field in required_fields:
                if field not in result:
                    logger.warning(f"Missing required field: {field}, setting default value")
                    if field == 'category':
                        result[field] = 'unknown'
                    elif field == 'confidence':
                        result[field] = 0.0
                    else:
                        result[field] = 'unknown'
            
            logger.info(f"Final parsed result: {json.dumps(result, indent=2)}")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}", exc_info=True)
            logger.error(f"Raw response that failed to parse: {response}")
            return {
                "classification": "personal",
                "confidence": 0.0,
                "reasoning": f"Error parsing response: {str(e)}",
                "category": "unknown"
            }
    
    def _parse_transaction_extraction_response(self, response: str) -> List[Dict[str, Any]]:
        logger.info(f"Parsing transaction extraction response: {response}")
        try:
            # Look for JSON array with brackets
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("No JSON array found in response")
                return []
            
            json_str = response[json_start:json_end]
            logger.info(f"Extracted JSON array string: {json_str}")
            
            transactions = json.loads(json_str)
            logger.info(f"Successfully parsed JSON array: {transactions}")
            
            # Validate each transaction
            validated_transactions = []
            for i, transaction in enumerate(transactions):
                logger.debug(f"Validating transaction {i + 1}: {transaction}")
                
                if isinstance(transaction, dict) and 'date' in transaction and 'description' in transaction and 'amount' in transaction:
                    # Ensure the amount is a valid number
                    try:
                        amount = float(transaction['amount'])
                        if amount == 0:
                            logger.warning(f"Transaction {i + 1} has zero amount, skipping")
                            continue
                    except (ValueError, TypeError):
                        logger.warning(f"Transaction {i + 1} has invalid amount: {transaction['amount']}, skipping")
                        continue
                    
                    validated_transaction = {
                        'date': transaction['date'],
                        'description': transaction['description'],
                        'amount': amount,
                        'currency': transaction.get('currency', 'USD'),
                        'merchant': transaction.get('merchant', '')
                    }
                    validated_transactions.append(validated_transaction)
                    logger.debug(f"Transaction {i + 1} validated: {validated_transaction}")
                else:
                    logger.warning(f"Transaction {i + 1} missing required fields: {transaction}")
            
            logger.info(f"Final validated transactions: {json.dumps(validated_transactions, indent=2)}")
            return validated_transactions
            
        except Exception as e:
            logger.error(f"Error parsing transaction extraction response: {str(e)}", exc_info=True)
            logger.error(f"Raw response that failed to parse: {response}")
            return []
    
    def batch_classify_transactions(self, transactions: list) -> list:
        """
        Classify multiple transactions (for future optimization)
        """
        results = []
        for transaction in transactions:
            result = self.classify_transaction(transaction)
            results.append(result)
        return results 