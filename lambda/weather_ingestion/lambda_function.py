import json
import os
import boto3
from datetime import datetime
from typing import Dict, Any
import requests
from utils import convert_to_parquet, create_s3_key

# Initialize AWS clients
s3_client = boto3.client('s3')

# Configuration from environment variables
# Note: Open-Meteo doesn't require API key
WEATHER_API_URL = os.environ.get('WEATHER_API_URL', 'https://api.open-meteo.com/v1/forecast')
S3_BUCKET = os.environ.get('S3_BUCKET')
LATITUDE = float(os.environ.get('LATITUDE', '51.5074'))  # Default: London
LONGITUDE = float(os.environ.get('LONGITUDE', '-0.1278'))  # Default: London
CITY = os.environ.get('CITY', 'London')  # For metadata only
COUNTRY_CODE = os.environ.get('COUNTRY_CODE', 'GB')  # For metadata only


def fetch_weather_data(latitude: float, longitude: float, api_url: str, city: str = None, country_code: str = None) -> Dict[str, Any]:
    """
    Fetch weather data from Open-Meteo API
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        api_url: Base URL for the API
        city: City name for metadata (optional)
        country_code: Country code for metadata (optional)
        
    Returns:
        Dictionary containing weather data
    """
    # Use provided values or fall back to module-level defaults
    city = city or CITY
    country_code = country_code or COUNTRY_CODE
    try:
        # Construct API request - Open-Meteo uses lat/long and specific parameters
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,wind_direction_10m,cloud_cover,visibility,weather_code',
            'timezone': 'auto',
            'forecast_days': 1
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Open-Meteo response structure
        current = data.get('current', {})
        
        # Map weather codes (WMO Weather interpretation codes)
        weather_code = current.get('weather_code', 0)
        weather_descriptions = {
            0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
            45: 'Foggy', 48: 'Depositing rime fog',
            51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
            56: 'Light freezing drizzle', 57: 'Dense freezing drizzle',
            61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
            66: 'Light freezing rain', 67: 'Heavy freezing rain',
            71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
            77: 'Snow grains', 80: 'Slight rain showers', 81: 'Moderate rain showers',
            82: 'Violent rain showers', 85: 'Slight snow showers', 86: 'Heavy snow showers',
            95: 'Thunderstorm', 96: 'Thunderstorm with slight hail', 99: 'Thunderstorm with heavy hail'
        }
        
        weather_main = 'Clear' if weather_code in [0, 1] else 'Clouds' if weather_code in [2, 3] else 'Rain' if weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82] else 'Snow' if weather_code in [71, 73, 75, 77, 85, 86] else 'Thunderstorm' if weather_code in [95, 96, 99] else 'Other'
        
        # Add metadata
        weather_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'city': city,
            'country_code': country_code,
            'weather_id': weather_code,
            'weather_main': weather_main,
            'weather_description': weather_descriptions.get(weather_code, 'Unknown'),
            'temperature': current.get('temperature_2m'),
            'feels_like': current.get('apparent_temperature'),
            'temp_min': current.get('temperature_2m'),  # Open-Meteo current doesn't provide min/max separately
            'temp_max': current.get('temperature_2m'),
            'pressure': int(current.get('pressure_msl', 0)) if current.get('pressure_msl') else None,
            'humidity': int(current.get('relative_humidity_2m', 0)) if current.get('relative_humidity_2m') else None,
            'visibility': int(current.get('visibility', 0) / 1000) if current.get('visibility') else None,  # Convert m to km
            'wind_speed': current.get('wind_speed_10m'),
            'wind_deg': current.get('wind_direction_10m'),
            'clouds': int(current.get('cloud_cover', 0)) if current.get('cloud_cover') else None,
            'sunrise': None,  # Open-Meteo current doesn't provide sunrise/sunset
            'sunset': None,
            'timezone': data.get('timezone', 'UTC'),
            'latitude': latitude,
            'longitude': longitude,
        }
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch weather data: {str(e)}")
    except KeyError as e:
        raise Exception(f"Unexpected API response format: {str(e)}")


def lambda_handler(event, context):
    """
    AWS Lambda handler function
    
    Args:
        event: Lambda event (can contain latitude, longitude, city, country_code override)
        context: Lambda context
        
    Returns:
        Dictionary with statusCode and body
    """
    try:
        # Get coordinates and metadata from event or use defaults
        latitude = float(event.get('latitude', LATITUDE)) if isinstance(event, dict) else LATITUDE
        longitude = float(event.get('longitude', LONGITUDE)) if isinstance(event, dict) else LONGITUDE
        city = event.get('city', CITY) if isinstance(event, dict) else CITY
        country_code = event.get('country_code', COUNTRY_CODE) if isinstance(event, dict) else COUNTRY_CODE
        
        # Validate required environment variables
        if not S3_BUCKET:
            raise ValueError("S3_BUCKET environment variable is not set")
        
        # Fetch weather data
        print(f"Fetching weather data for {city}, {country_code} (lat: {latitude}, lon: {longitude})")
        weather_data = fetch_weather_data(latitude, longitude, WEATHER_API_URL, city, country_code)
        
        # Convert to Parquet format
        print("Converting data to Parquet format")
        parquet_data = convert_to_parquet([weather_data])
        
        # Create S3 key with partitioning (year/month/day/hour)
        s3_key = create_s3_key(city, country_code)
        
        # Upload to S3
        print(f"Uploading to s3://{S3_BUCKET}/{s3_key}")
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=parquet_data,
            ContentType='application/octet-stream'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Weather data successfully ingested',
                'city': city,
                'country_code': country_code,
                'latitude': latitude,
                'longitude': longitude,
                's3_location': f's3://{S3_BUCKET}/{s3_key}',
                'timestamp': weather_data['timestamp']
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to ingest weather data'
            })
        }

