import boto3
import os
from typing import Optional

# Initialize DynamoDB
def get_dynamodb_resource():
    """Get DynamoDB resource"""
    # Use environment variable or default
    region = os.getenv('AWS_REGION', 'eu-west-2')
    
    # In Lambda, credentials are handled automatically
    # For local testing, you might need to configure credentials
    return boto3.resource('dynamodb', region_name=region)

def get_dynamodb_table(table_name: Optional[str] = None):
    """Get DynamoDB table"""
    if not table_name:
        table_name = os.getenv('DYNAMODB_TABLE', 'parsea-transactions')
    
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)

# For backward compatibility, create a simple session manager
class DynamoDBSession:
    """Simple session manager for DynamoDB operations"""
    
    def __init__(self):
        self.table = get_dynamodb_table()
    
    def close(self):
        """No-op for DynamoDB"""
        pass

def get_db():
    """
    Dependency to get database session (DynamoDB compatible)
    """
    session = DynamoDBSession()
    try:
        yield session
    finally:
        session.close() 