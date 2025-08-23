import json
import os
from mangum import Mangum
from app.main import app

# Create handler for Lambda
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    Lambda handler that uses Mangum to convert between Lambda and ASGI.
    
    CORS is handled by:
    1. FastAPI's CORSMiddleware in app.main
    2. API Gateway CORS configuration in template.yaml
    
    No manual CORS headers needed here to avoid duplicates.
    """
    # Process the request through Mangum
    # Mangum will properly convert FastAPI's CORS headers
    response = handler(event, context)
    
    return response 