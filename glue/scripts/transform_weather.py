"""
AWS Glue ETL Script for Weather Data Transformation
This script can be used to transform, clean, or aggregate weather data
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'DATABASE_NAME', 'TABLE_NAME', 'OUTPUT_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get parameters
database_name = args['DATABASE_NAME']
table_name = args['TABLE_NAME']
output_path = args.get('OUTPUT_PATH', 's3://your-bucket/transformed/')

# Read data from Glue catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database=database_name,
    table_name=table_name,
    transformation_ctx="datasource"
)

# Example transformations
# 1. Filter data (e.g., only records with temperature > 0)
def filter_positive_temp(record):
    return record.get("temperature", 0) > 0

filtered_dyf = Filter.apply(
    frame=datasource,
    f=filter_positive_temp,
    transformation_ctx="filtered"
)

# 2. Add calculated fields (e.g., temperature in Fahrenheit)
def add_fahrenheit(record):
    temp_c = record.get("temperature", 0)
    record["temperature_f"] = (temp_c * 9/5) + 32
    return record

transformed_dyf = Map.apply(
    frame=filtered_dyf,
    f=add_fahrenheit,
    transformation_ctx="transformed"
)

# Convert to Spark DataFrame for more complex operations if needed
df = transformed_dyf.toDF()

# Example: Aggregate by hour
# df_hourly = df.groupBy("year", "month", "day", "hour").agg({
#     "temperature": "avg",
#     "humidity": "avg",
#     "pressure": "avg"
# })

# Convert back to DynamicFrame
final_dyf = DynamicFrame.fromDF(df, glueContext, "final_dyf")

# Write to S3 in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=final_dyf,
    connection_type="s3",
    connection_options={
        "path": output_path,
        "partitionKeys": ["year", "month", "day", "hour"]
    },
    format="parquet",
    transformation_ctx="datasink"
)

job.commit()

