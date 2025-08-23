import uuid
import boto3
from datetime import datetime
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError
from ..database import get_dynamodb_table
from ..utils.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)

class UserService:
    """DynamoDB-based user service"""
    
    def __init__(self):
        self.table = get_dynamodb_table()
    
    def create_user(self, email: str, password: str, full_name: str, 
                   business_name: str = None, business_type: str = None) -> Dict[str, Any]:
        """Create a new user"""
        try:
            user_id = str(uuid.uuid4())
            password_hash = get_password_hash(password)
            
            # Create user item
            user_item = {
                'id': user_id,
                'user_id': user_id,  # For compatibility with table schema
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name,
                'business_name': business_name or '',
                'business_type': business_type or '',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'type': 'user'  # To distinguish from transactions
            }
            
            # Check if user already exists
            existing_user = self.get_user_by_email(email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Create user in DynamoDB
            self.table.put_item(Item=user_item)
            
            logger.info(f"User created successfully: {email}")
            
            # Return user without password hash
            user_item.pop('password_hash', None)
            return user_item
            
        except ClientError as e:
            logger.error(f"DynamoDB error creating user: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            # Scan for user by email (in production, consider using GSI)
            response = self.table.scan(
                FilterExpression='email = :email AND #type = :type',
                ExpressionAttributeValues={
                    ':email': email,
                    ':type': 'user'
                },
                ExpressionAttributeNames={
                    '#type': 'type'
                }
            )
            
            items = response.get('Items', [])
            if items:
                return items[0]
            return None
            
        except ClientError as e:
            logger.error(f"DynamoDB error getting user by email: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            response = self.table.get_item(
                Key={
                    'id': user_id,
                    'user_id': user_id
                }
            )
            
            return response.get('Item')
            
        except ClientError as e:
            logger.error(f"DynamoDB error getting user by ID: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        try:
            user = self.get_user_by_email(email)
            if not user:
                logger.info(f"Authentication failed: user not found for {email}")
                return None
            
            if not verify_password(password, user['password_hash']):
                logger.info(f"Authentication failed: incorrect password for {email}")
                return None
            
            logger.info(f"User authenticated successfully: {email}")
            
            # Return user without password hash
            user.pop('password_hash', None)
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    def update_user(self, user_id: str, **updates) -> bool:
        """Update user information"""
        try:
            # Build update expression
            update_expression = "SET updated_at = :updated_at"
            expression_values = {':updated_at': datetime.utcnow().isoformat()}
            
            for key, value in updates.items():
                if key not in ['id', 'user_id', 'created_at']:
                    update_expression += f", {key} = :{key}"
                    expression_values[f":{key}"] = value
            
            self.table.update_item(
                Key={
                    'id': user_id,
                    'user_id': user_id
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            
            logger.info(f"User updated successfully: {user_id}")
            return True
            
        except ClientError as e:
            logger.error(f"DynamoDB error updating user: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False 