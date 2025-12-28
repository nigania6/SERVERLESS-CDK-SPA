#!/usr/bin/env python3
import os
import aws_cdk as cdk
from infrastructure.stack import WeatherPipelineStack

app = cdk.App()

# Get environment variables or use defaults
env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION', 'us-east-1')
)

# Create the stack
WeatherPipelineStack(
    app,
    "WeatherPipelineStack",
    env=env,
    description="Weather data pipeline with Lambda, S3, Glue, and Athena"
)

app.synth()

