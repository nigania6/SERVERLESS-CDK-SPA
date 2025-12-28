import io
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def convert_to_parquet(data: List[Dict[str, Any]]) -> bytes:
    """
    Convert a list of dictionaries to Parquet format
    
    Args:
        data: List of dictionaries containing weather data
        
    Returns:
        bytes: Parquet file as bytes
    """
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Ensure timestamp is datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Convert DataFrame to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Write to Parquet format in memory
    buffer = io.BytesIO()
    pq.write_table(table, buffer, compression='snappy')
    
    # Return bytes
    return buffer.getvalue()


def create_s3_key(city: str, country_code: str, timestamp: datetime = None) -> str:
    """
    Create S3 key with partitioning structure: year=YYYY/month=MM/day=DD/hour=HH/filename.parquet
    
    Args:
        city: City name
        country_code: Country code
        timestamp: Optional timestamp (defaults to current UTC time)
        
    Returns:
        S3 key string
    """
    if timestamp is None:
        timestamp = datetime.utcnow()
    
    # Format: year=YYYY/month=MM/day=DD/hour=HH/city_country_timestamp.parquet
    year = timestamp.strftime('%Y')
    month = timestamp.strftime('%m')
    day = timestamp.strftime('%d')
    hour = timestamp.strftime('%H')
    
    # Create filename with timestamp for uniqueness
    filename = f"{city.lower().replace(' ', '_')}_{country_code.lower()}_{timestamp.strftime('%Y%m%d_%H%M%S')}.parquet"
    
    s3_key = f"year={year}/month={month}/day={day}/hour={hour}/{filename}"
    
    return s3_key

