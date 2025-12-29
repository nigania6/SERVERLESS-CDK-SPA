from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    RemovalPolicy,
    BundlingOptions,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    aws_glue as glue,
)
from constructs import Construct
import os


class WeatherPipelineStack(Stack):
    """Main CDK stack for Weather Data Pipeline"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Stage 2: Weather API Integration
        
        # Create S3 bucket for weather data
        weather_bucket = s3.Bucket(
            self,
            "WeatherDataBucket",
            bucket_name=f"weather-data-{self.account}-{self.region}",
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN,  # Retain bucket on stack deletion
            auto_delete_objects=False,
        )
        
        # Get coordinates from context or use defaults (London)
        # Open-Meteo doesn't require API key
        latitude = float(self.node.try_get_context("latitude") or os.getenv("LATITUDE", "51.5074"))
        longitude = float(self.node.try_get_context("longitude") or os.getenv("LONGITUDE", "-0.1278"))
        
        # Create Lambda function for weather ingestion
        # Use Docker bundling with exclusions to reduce package size
        weather_lambda = lambda_.Function(
            self,
            "WeatherIngestionFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset(
                "lambda/weather_ingestion",
                bundling=BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash", "-c",
                        "cp -r /asset-input/* /asset-output/ && "
                        "pip install --no-cache-dir -r /asset-output/requirements.txt -t /asset-output && "
                        "find /asset-output -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && "
                        "find /asset-output -type f -name '*.pyc' -delete && "
                        "find /asset-output -type f -name '*.pyo' -delete && "
                        "find /asset-output -type d -name '*.dist-info' -exec rm -rf {} + 2>/dev/null || true && "
                        "find /asset-output -type d -name 'tests' -exec rm -rf {} + 2>/dev/null || true && "
                        "find /asset-output -type d -name 'test' -exec rm -rf {} + 2>/dev/null || true && "
                        "find /asset-output -type d -name 'doc' -exec rm -rf {} + 2>/dev/null || true && "
                        "find /asset-output -type d -name 'docs' -exec rm -rf {} + 2>/dev/null || true && "
                        "find /asset-output -type f -name '*.md' -delete && "
                        "find /asset-output -type f -name '*.txt' ! -name 'requirements.txt' -delete && "
                        "find /asset-output -type f -name 'LICENSE*' -delete && "
                        "find /asset-output -type f -name '*.so.*' -delete"
                    ],
                ),
            ),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "WEATHER_API_URL": "https://api.open-meteo.com/v1/forecast",
                "S3_BUCKET": weather_bucket.bucket_name,
                "LATITUDE": str(latitude),
                "LONGITUDE": str(longitude),
                "CITY": self.node.try_get_context("city") or "London",
                "COUNTRY_CODE": self.node.try_get_context("country_code") or "GB",
            },
        )
        
        # Grant Lambda permission to write to S3 bucket
        weather_bucket.grant_write(weather_lambda)
        
        # Stage 3: EventBridge Schedule - Trigger Lambda every minute
        event_rule = events.Rule(
            self,
            "WeatherIngestionSchedule",
            description="Trigger weather ingestion Lambda every minute",
            schedule=events.Schedule.rate(Duration.minutes(1)),
            enabled=True,
        )
        event_rule.add_target(targets.LambdaFunction(weather_lambda))
        
        # Stage 5: Glue Catalog & Table (No Crawler)
        # Create Glue Database
        glue_database = glue.CfnDatabase(
            self,
            "WeatherDatabase",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name=f"weather_db_{self.stack_name.lower()}",
                description="Database for weather data"
            )
        )
        
        # Create Glue Table for weather data
        # Define schema based on the Lambda function output
        glue_table = glue.CfnTable(
            self,
            "WeatherDataTable",
            catalog_id=self.account,
            database_name=glue_database.database_input.name,
            table_input=glue.CfnTable.TableInputProperty(
                name="weather_data",
                description="Weather data table with Parquet format",
                table_type="EXTERNAL_TABLE",
                parameters={
                    "classification": "parquet",
                    "typeOfData": "file"
                },
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    columns=[
                        glue.CfnTable.ColumnProperty(name="timestamp", type="timestamp", comment="Data collection timestamp"),
                        glue.CfnTable.ColumnProperty(name="city", type="string", comment="City name"),
                        glue.CfnTable.ColumnProperty(name="country_code", type="string", comment="Country code"),
                        glue.CfnTable.ColumnProperty(name="weather_id", type="int", comment="Weather condition ID"),
                        glue.CfnTable.ColumnProperty(name="weather_main", type="string", comment="Weather main condition"),
                        glue.CfnTable.ColumnProperty(name="weather_description", type="string", comment="Weather description"),
                        glue.CfnTable.ColumnProperty(name="temperature", type="double", comment="Temperature in Celsius"),
                        glue.CfnTable.ColumnProperty(name="feels_like", type="double", comment="Feels like temperature"),
                        glue.CfnTable.ColumnProperty(name="temp_min", type="double", comment="Minimum temperature"),
                        glue.CfnTable.ColumnProperty(name="temp_max", type="double", comment="Maximum temperature"),
                        glue.CfnTable.ColumnProperty(name="pressure", type="int", comment="Atmospheric pressure"),
                        glue.CfnTable.ColumnProperty(name="humidity", type="int", comment="Humidity percentage"),
                        glue.CfnTable.ColumnProperty(name="visibility", type="int", comment="Visibility in meters"),
                        glue.CfnTable.ColumnProperty(name="wind_speed", type="double", comment="Wind speed"),
                        glue.CfnTable.ColumnProperty(name="wind_deg", type="int", comment="Wind direction in degrees"),
                        glue.CfnTable.ColumnProperty(name="clouds", type="int", comment="Cloud coverage percentage"),
                        glue.CfnTable.ColumnProperty(name="sunrise", type="bigint", comment="Sunrise timestamp"),
                        glue.CfnTable.ColumnProperty(name="sunset", type="bigint", comment="Sunset timestamp"),
                        glue.CfnTable.ColumnProperty(name="timezone", type="string", comment="Timezone"),
                        glue.CfnTable.ColumnProperty(name="latitude", type="double", comment="Latitude"),
                        glue.CfnTable.ColumnProperty(name="longitude", type="double", comment="Longitude"),
                    ],
                    location=f"s3://{weather_bucket.bucket_name}/",
                    input_format="org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                    output_format="org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library="org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
                        parameters={
                            "serialization.format": "1"
                        }
                ),
                    compressed=False,
                    stored_as_sub_directories=True
            ),
                partition_keys=[
                    glue.CfnTable.ColumnProperty(name="year", type="string", comment="Year partition"),
                    glue.CfnTable.ColumnProperty(name="month", type="string", comment="Month partition"),
                    glue.CfnTable.ColumnProperty(name="day", type="string", comment="Day partition"),
                    glue.CfnTable.ColumnProperty(name="hour", type="string", comment="Hour partition"),
                ]
            )
        )
        glue_table.add_dependency(glue_database)
        
        # Output stack information
        CfnOutput(
            self,
            "StackName",
            value=self.stack_name,
            description="Name of the CDK stack"
        )
        
        CfnOutput(
            self,
            "Region",
            value=self.region,
            description="AWS Region where resources are deployed"
        )
        
        CfnOutput(
            self,
            "WeatherDataBucketOutput",
            value=weather_bucket.bucket_name,
            description="S3 bucket for weather data storage"
        )
        
        CfnOutput(
            self,
            "WeatherLambdaFunctionArn",
            value=weather_lambda.function_arn,
            description="ARN of the weather ingestion Lambda function"
        )
        
        CfnOutput(
            self,
            "WeatherLambdaFunctionName",
            value=weather_lambda.function_name,
            description="Name of the weather ingestion Lambda function"
        )
        
        CfnOutput(
            self,
            "EventBridgeRuleName",
            value=event_rule.rule_name,
            description="EventBridge rule that triggers Lambda every minute"
        )
        
        CfnOutput(
            self,
            "GlueDatabaseName",
            value=glue_database.database_input.name,
            description="Glue database name for weather data"
        )
        
        CfnOutput(
            self,
            "GlueTableName",
            value=glue_table.table_input.name,
            description="Glue table name for weather data"
        )
        
        CfnOutput(
            self,
            "AthenaQueryExample",
            value=f"SELECT * FROM {glue_database.database_input.name}.{glue_table.table_input.name} LIMIT 10",
            description="Example Athena query"
        )

