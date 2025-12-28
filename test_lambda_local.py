#!/usr/bin/env python3
"""
Local testing script for the weather ingestion Lambda function
Run this to test the Lambda function locally before deploying
"""

import os
import sys
import json

# Add lambda directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lambda', 'weather_ingestion'))
from lambda_function import lambda_handler

# Set up environment variables for local testing
# Open-Meteo doesn't require API key
os.environ['WEATHER_API_URL'] = 'https://api.open-meteo.com/v1/forecast'
os.environ['S3_BUCKET'] = 'test-weather-bucket'  # Will fail on S3 upload, but tests API call
os.environ['LATITUDE'] = '51.5074'  # London
os.environ['LONGITUDE'] = '-0.1278'  # London
os.environ['CITY'] = 'London'
os.environ['COUNTRY_CODE'] = 'GB'

# Mock event
event = {
    'city': 'London',
    'country_code': 'GB',
    'latitude': 51.5074,
    'longitude': -0.1278
}

# Mock context (minimal implementation)
class MockContext:
    def __init__(self):
        self.function_name = 'test-weather-ingestion'
        self.function_version = '$LATEST'
        self.memory_limit_in_mb = 256
        self.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:test'
        self.aws_request_id = 'test-request-id'

if __name__ == '__main__':
    print("Testing Weather Ingestion Lambda Function Locally")
    print("=" * 50)
    print("Using Open-Meteo API (no API key required)")
    print(f"City: {event['city']}, Country: {event['country_code']}")
    print(f"Coordinates: {event['latitude']}, {event['longitude']}")
    print()
    
    try:
        context = MockContext()
        result = lambda_handler(event, context)
        
        print("Lambda Execution Result:")
        print(json.dumps(result, indent=2))
        
        if result['statusCode'] == 200:
            print("\n✅ Test passed! Lambda function executed successfully")
            print("Note: S3 upload will fail in local test (expected)")
        else:
            print("\n❌ Test failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

