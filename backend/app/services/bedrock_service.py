import boto3
import json
from typing import Dict, Any, List
import logging
from datetime import datetime
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
    
    def classify_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a transaction using AWS Bedrock Claude
        """
        request_id = f"classify_{datetime.now().strftime('%H%M%S%f')[:-3]}"
        logger.info(f"[{request_id}] Starting transaction classification - Data: {transaction_data}")
        start_time = datetime.now()
        
        prompt = self._build_classification_prompt(transaction_data)
        logger.debug(f"[{request_id}] Classification prompt built - Length: {len(prompt)} characters")
        logger.debug(f"[{request_id}] Full classification prompt:\n{prompt}")
        
        try:
            # Prepare the request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,  # Increased from 200 to 500
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
            
            logger.info(f"[{request_id}] Classification completed successfully - Result: {result}, Time: {processing_time:.3f}s")
            logger.info(f"[{request_id}] Parsed result: {json.dumps(result, indent=2)}")
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
    
    def extract_transactions_from_pdf(self, pdf_text: str) -> List[Dict[str, Any]]:
        """
        Extract transactions from PDF bank statement text using AWS Bedrock Claude
        """
        request_id = f"extract_{datetime.now().strftime('%H%M%S%f')[:-3]}"
        logger.info(f"[{request_id}] Starting PDF transaction extraction - Text length: {len(pdf_text)} characters")
        start_time = datetime.now()
        
        prompt = self._build_pdf_extraction_prompt(pdf_text)
        logger.debug(f"[{request_id}] PDF extraction prompt built - Length: {len(prompt)} characters")
        logger.debug(f"[{request_id}] Full PDF extraction prompt:\n{prompt}")
        
        try:
            # Prepare the request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,  # Increased from 1000 to 2000 for longer responses
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
            # Try multiple JSON extraction strategies
            result = None
            
            # Strategy 1: Look for JSON object with braces
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                try:
                    json_str = response[json_start:json_end]
                    logger.debug(f"Strategy 1 - Extracted JSON string: {json_str}")
                    result = json.loads(json_str)
                    logger.info(f"Strategy 1 successful - Parsed JSON: {result}")
                except json.JSONDecodeError as e:
                    logger.warning(f"Strategy 1 failed - JSON decode error: {e}")
                    result = None
            
            # Strategy 2: Look for JSON object with quotes and braces (more flexible)
            if result is None:
                # Find the first occurrence of a pattern that looks like JSON
                import re
                json_pattern = r'\{[^{}]*"[^"]*"[^{}]*\}'
                matches = re.findall(json_pattern, response)
                if matches:
                    try:
                        json_str = matches[0]
                        logger.debug(f"Strategy 2 - Extracted JSON string: {json_str}")
                        result = json.loads(json_str)
                        logger.info(f"Strategy 2 successful - Parsed JSON: {result}")
                    except json.JSONDecodeError as e:
                        logger.warning(f"Strategy 2 failed - JSON decode error: {e}")
                        result = None
            
            # Strategy 3: Look for key-value pairs and construct JSON manually
            if result is None:
                logger.debug("Strategy 3 - Attempting manual JSON construction from key-value pairs")
                result = self._construct_json_from_text(response)
                if result:
                    logger.info(f"Strategy 3 successful - Constructed JSON: {result}")
            
            if result is None:
                logger.error("All JSON extraction strategies failed")
                raise ValueError("Could not extract valid JSON from response")
            
            # Validate and fill missing fields
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
            # Try multiple JSON extraction strategies
            transactions = None
            
            # Strategy 1: Look for JSON array with brackets
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                try:
                    json_str = response[json_start:json_end]
                    logger.info(f"Strategy 1 - Extracted JSON array string: {json_str}")
                    transactions = json.loads(json_str)
                    logger.info(f"Strategy 1 successful - Parsed JSON array: {transactions}")
                except json.JSONDecodeError as e:
                    logger.warning(f"Strategy 1 failed - JSON decode error: {e}")
                    transactions = None
            
            # Strategy 2: Look for multiple JSON objects
            if transactions is None:
                logger.debug("Strategy 2 - Looking for multiple JSON objects")
                import re
                json_objects = re.findall(r'\{[^{}]*"[^"]*"[^{}]*\}', response)
                if json_objects:
                    try:
                        transactions = []
                        for obj_str in json_objects:
                            obj = json.loads(obj_str)
                            if 'date' in obj and 'description' in obj and 'amount' in obj:
                                transactions.append(obj)
                        logger.info(f"Strategy 2 successful - Found {len(transactions)} JSON objects")
                    except json.JSONDecodeError as e:
                        logger.warning(f"Strategy 2 failed - JSON decode error: {e}")
                        transactions = None
            
            # Strategy 3: Manual parsing from text
            if transactions is None:
                logger.debug("Strategy 3 - Attempting manual parsing from text")
                transactions = self._extract_transactions_from_text(response)
                if transactions:
                    logger.info(f"Strategy 3 successful - Manually extracted {len(transactions)} transactions")
            
            if transactions is None:
                logger.error("All transaction extraction strategies failed")
                return []
            
            # Validate and clean each transaction
            validated_transactions = []
            for i, transaction in enumerate(transactions):
                logger.debug(f"Validating transaction {i + 1}: {transaction}")
                
                # Clean the transaction data
                cleaned_transaction = self._clean_transaction_data(transaction)
                
                if isinstance(cleaned_transaction, dict) and 'date' in cleaned_transaction and 'description' in cleaned_transaction and 'amount' in cleaned_transaction:
                    # Ensure the amount is a valid number
                    try:
                        amount = float(cleaned_transaction['amount'])
                        if amount == 0:
                            logger.warning(f"Transaction {i + 1} has zero amount, skipping")
                            continue
                    except (ValueError, TypeError):
                        logger.warning(f"Transaction {i + 1} has invalid amount: {cleaned_transaction['amount']}, skipping")
                        continue
                    
                    validated_transaction = {
                        'date': cleaned_transaction['date'],
                        'description': cleaned_transaction['description'],
                        'amount': amount,
                        'currency': cleaned_transaction.get('currency', 'USD'),
                        'merchant': cleaned_transaction.get('merchant', '')
                    }
                    validated_transactions.append(validated_transaction)
                    logger.debug(f"Transaction {i + 1} validated: {validated_transaction}")
                else:
                    logger.warning(f"Transaction {i + 1} missing required fields: {cleaned_transaction}")
            
            logger.info(f"Final validated transactions: {json.dumps(validated_transactions, indent=2)}")
            return validated_transactions
            
        except Exception as e:
            logger.error(f"Error parsing transaction extraction response: {str(e)}", exc_info=True)
            logger.error(f"Raw response that failed to parse: {response}")
            return []
    
    def _clean_transaction_data(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate transaction data to prevent nested JSON issues"""
        logger.debug(f"Cleaning transaction data: {transaction}")
        try:
            cleaned = {}
            
            # Handle date field
            if 'date' in transaction:
                date_val = transaction['date']
                logger.debug(f"Processing date field: {date_val} (type: {type(date_val)})")
                if isinstance(date_val, str) and date_val.strip():
                    # Validate date format (YYYY-MM-DD)
                    import re
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
                        cleaned['date'] = date_val
                        logger.debug(f"Date validated: {date_val}")
                    else:
                        logger.warning(f"Invalid date format: {date_val}, setting to today")
                        from datetime import datetime
                        cleaned['date'] = datetime.now().strftime('%Y-%m-%d')
                else:
                    logger.warning(f"Empty or invalid date: {date_val}, setting to today")
                    from datetime import datetime
                    cleaned['date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Handle description field
            if 'description' in transaction:
                desc_val = transaction['description']
                logger.debug(f"Processing description field: {desc_val} (type: {type(desc_val)})")
                if isinstance(desc_val, str):
                    # Remove any JSON artifacts or extra characters
                    desc_val = desc_val.strip()
                    if desc_val.startswith('{') and desc_val.endswith('}'):
                        logger.warning(f"Description contains JSON: {desc_val}, extracting text content")
                        try:
                            # Try to extract meaningful text from the JSON
                            json_obj = json.loads(desc_val)
                            logger.debug(f"Parsed JSON from description: {json_obj}")
                            if 'description' in json_obj:
                                desc_val = json_obj['description']
                                logger.debug(f"Extracted description from JSON: {desc_val}")
                            elif 'merchant' in json_obj:
                                desc_val = json_obj['merchant']
                                logger.debug(f"Extracted merchant as description: {desc_val}")
                            else:
                                desc_val = "Transaction description"
                        except Exception as e:
                            logger.error(f"Failed to parse JSON from description: {e}")
                            desc_val = "Transaction description"
                    
                    # Clean up common artifacts
                    desc_val = desc_val.replace('",', '').replace('"', '').strip()
                    cleaned['description'] = desc_val
                    logger.debug(f"Final cleaned description: {desc_val}")
                else:
                    cleaned['description'] = str(desc_val)
            
            # Handle amount field
            if 'amount' in transaction:
                amount_val = transaction['amount']
                logger.debug(f"Processing amount field: {amount_val} (type: {type(amount_val)})")
                if isinstance(amount_val, (int, float)):
                    cleaned['amount'] = amount_val
                    logger.debug(f"Amount is numeric: {amount_val}")
                elif isinstance(amount_val, str):
                    # Clean amount string and convert to float
                    amount_str = amount_val.strip().replace(',', '').replace('$', '').replace('£', '').replace('€', '')
                    logger.debug(f"Cleaned amount string: '{amount_str}'")
                    try:
                        cleaned['amount'] = float(amount_str)
                        logger.debug(f"Amount converted to float: {cleaned['amount']}")
                    except ValueError:
                        logger.error(f"Invalid amount value: {amount_val}")
                        return None
                else:
                    logger.error(f"Unexpected amount type: {type(amount_val)} for value: {amount_val}")
                    return None
            
            # Handle currency field
            if 'currency' in transaction:
                currency_val = transaction['currency']
                if isinstance(currency_val, str) and currency_val.strip():
                    cleaned['currency'] = currency_val.strip().upper()
                else:
                    cleaned['currency'] = 'USD'
            
            # Handle merchant field
            if 'merchant' in transaction:
                merchant_val = transaction['merchant']
                if isinstance(merchant_val, str) and merchant_val.strip():
                    cleaned['merchant'] = merchant_val.strip()
                else:
                    cleaned['merchant'] = ''
            
            logger.debug(f"Final cleaned transaction: {cleaned}")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning transaction data: {str(e)}")
            return None
    
    def _construct_json_from_text(self, text: str) -> Dict[str, Any]:
        """Manually construct JSON from text when parsing fails"""
        try:
            result = {}
            
            # Look for classification
            if 'business' in text.lower():
                result['classification'] = 'business'
            elif 'personal' in text.lower():
                result['classification'] = 'personal'
            else:
                result['classification'] = 'personal'
            
            # Look for confidence
            import re
            confidence_match = re.search(r'confidence[:\s]*(\d*\.?\d*)', text.lower())
            if confidence_match:
                try:
                    result['confidence'] = float(confidence_match.group(1))
                except:
                    result['confidence'] = 0.5
            else:
                result['confidence'] = 0.5
            
            # Look for reasoning
            reasoning_match = re.search(r'reasoning[:\s]*(.+?)(?=\n|$)', text.lower())
            if reasoning_match:
                result['reasoning'] = reasoning_match.group(1).strip()
            else:
                result['reasoning'] = 'Extracted from text analysis'
            
            # Look for category
            category_match = re.search(r'category[:\s]*(\w+)', text.lower())
            if category_match:
                result['category'] = category_match.group(1)
            else:
                result['category'] = 'unknown'
            
            return result
        except Exception as e:
            logger.error(f"Error constructing JSON from text: {str(e)}")
            return None
    
    def _extract_transactions_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Manually extract transactions from text when JSON parsing fails"""
        try:
            transactions = []
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for date patterns
                import re
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                if date_match:
                    # Try to extract amount and description
                    amount_match = re.search(r'([+-]?\d+\.?\d*)', line)
                    if amount_match:
                        transaction = {
                            'date': date_match.group(1),
                            'description': line.replace(date_match.group(1), '').replace(amount_match.group(1), '').strip(),
                            'amount': float(amount_match.group(1)),
                            'currency': 'USD',
                            'merchant': ''
                        }
                        transactions.append(transaction)
            
            return transactions
        except Exception as e:
            logger.error(f"Error extracting transactions from text: {str(e)}")
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