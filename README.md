# Weather Data Pipeline - AWS CDK Project

A serverless data pipeline that ingests weather data from a free API, stores it in S3 as Parquet files, processes with AWS Glue, and enables querying via Athena - all without using Glue Crawler.

## Architecture

```
Weather API → Lambda (Every 1 min) → S3 (Parquet) → Glue Table → Athena Queries
```

## Prerequisites

Before you begin, ensure you have:

- **AWS Account** with appropriate permissions
- **AWS CLI** installed and configured (`aws configure`)
- **Python 3.9+** installed
- **Node.js 18+** installed (required for AWS CDK)
- **Git** installed
- **Coordinates** (latitude/longitude) for weather location (defaults to London: 51.5074, -0.1278)

## Stage 1: Project Setup

### Step 1: Clone/Initialize Project

If you haven't already, initialize the project in this directory.

### Step 2: Run Setup Script

**For Windows:**
```bash
setup.bat
```

**For Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python -m venv venv  # or python3 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure AWS Credentials

Make sure your AWS credentials are configured:

```bash
aws configure
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (e.g., `json`)

### Step 4: Bootstrap CDK (First Time Only)

If this is your first time using CDK in this AWS account/region:

```bash
cdk bootstrap
```

This creates the necessary S3 bucket and IAM roles for CDK deployments.

### Step 5: Verify Setup

Check that everything is installed correctly:

```bash
# Verify CDK
cdk --version

# Verify Python packages
pip list | grep aws-cdk

# Verify AWS CLI
aws --version
```

## Project Structure

```
cdk-weather-glue/
├── app.py                          # CDK app entry point
├── cdk.json                        # CDK configuration
├── requirements.txt                # Python dependencies
├── setup.sh / setup.bat           # Environment setup scripts
├── todo.md                         # Project todo list
├── README.md                       # This file
│
├── infrastructure/
│   ├── __init__.py
│   └── stack.py                    # Main CDK stack
│
├── lambda/                         # (To be created in Stage 2)
│   └── weather_ingestion/
│
├── glue/                           # (To be created in Stage 5)
│   └── scripts/
│
└── .github/                        # (To be created in Stage 8)
    └── workflows/
```

## Common CDK Commands

```bash
# Synthesize CloudFormation template
cdk synth

# Compare deployed stack with current state
cdk diff

# Deploy this stack to your default AWS account/region
cdk deploy

# Destroy the stack
cdk destroy

# List all stacks
cdk list
```

## Stage 2: Weather API Integration

### Prerequisites
- Stage 1 completed
- **No API key required!** This project uses [Open-Meteo](https://open-meteo.com/) - a free, open-source weather API

### Step 1: Set Location Coordinates (Optional)

**Option 1: Via CDK Context (Recommended)**
```bash
cdk deploy -c latitude=51.5074 -c longitude=-0.1278 -c city=London -c country_code=GB
```

**Option 2: Via Environment Variables**
```bash
export LATITUDE=51.5074
export LONGITUDE=-0.1278
export CITY=London
export COUNTRY_CODE=GB
cdk deploy
```

**Option 3: Use Defaults (London)**
```bash
# Just deploy - defaults to London coordinates
cdk deploy
```

### Step 2: Deploy Stage 2

```bash
# Synthesize to check for errors
cdk synth

# Deploy the stack
cdk deploy
```

### Step 3: Test Lambda Function Locally (Optional)

```bash
# No API key needed! Open-Meteo is free
# Run local test
python test_lambda_local.py
```

### Step 4: Test Lambda Function in AWS

After deployment, you can test the Lambda function:

```bash
# Invoke Lambda function
aws lambda invoke \
  --function-name <WeatherLambdaFunctionName> \
  --payload '{"city":"London","country_code":"GB","latitude":51.5074,"longitude":-0.1278}' \
  response.json

# View response
cat response.json
```

### What's Created in Stage 2

- **S3 Bucket**: `weather-data-{account}-{region}` for storing Parquet files
- **Lambda Function**: Weather ingestion function that:
  - Fetches data from Open-Meteo API (free, no API key required)
  - Converts JSON to Parquet format
  - Uploads to S3 with partitioning (year/month/day/hour)
- **IAM Permissions**: Lambda has write access to S3 bucket

## Complete Pipeline Overview

The pipeline consists of 9 stages, all of which are now implemented:

### ✅ Stage 1: Project Setup & Dependencies
- CDK project initialized
- Python virtual environment configured
- Dependencies installed

### ✅ Stage 2: Weather API Integration
- Lambda function created
- Weather data fetching implemented
- Parquet conversion working
- S3 upload with partitioning

### ✅ Stage 3: EventBridge Schedule
- EventBridge rule triggers Lambda every minute
- Automatic data ingestion enabled

### ✅ Stage 4: S3 Bucket Structure
- S3 bucket with encryption
- Partitioning structure: `year=YYYY/month=MM/day=DD/hour=HH/`

### ✅ Stage 5: Glue Catalog & Table (No Crawler)
- Glue database created
- Glue table with schema defined programmatically
- Parquet format configured
- Partition columns set up

### ✅ Stage 6: Glue ETL Job (Optional)
- ETL script available in `glue/scripts/transform_weather.py`
- Can be used for data transformations

### ✅ Stage 7: Athena Setup
- Table ready for querying
- Example queries in `athena_queries.sql`

### ✅ Stage 8: CI/CD with GitHub Actions
- GitHub Actions workflow configured
- Automated deployment on push to main

### ✅ Stage 9: Testing & Documentation
- Complete documentation
- Testing guides
- Example queries

## Deployment Guide

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured: `aws configure`
3. **Location coordinates** (latitude/longitude) - defaults to London if not specified
4. **GitHub Repository** (for CI/CD)

### Step-by-Step Deployment

#### 1. Initial Setup

```bash
# Run setup script
setup.bat  # Windows
# or
./setup.sh  # Linux/Mac

# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

#### 2. Install Lambda Dependencies

```bash
pip install -r lambda/weather_ingestion/requirements.txt -t lambda/weather_ingestion/
```

#### 3. Set Location Coordinates (Optional)

```bash
# Optional: Set coordinates (defaults to London)
export LATITUDE=51.5074
export LONGITUDE=-0.1278
export CITY=London
export COUNTRY_CODE=GB
```

Or use CDK context:
```bash
cdk deploy -c latitude=51.5074 -c longitude=-0.1278 -c city=London -c country_code=GB
```

**Note:** No API key needed! Open-Meteo is completely free.

#### 4. Bootstrap CDK (First Time Only)

```bash
cdk bootstrap
```

#### 5. Deploy Stack

```bash
# Synthesize to check for errors
cdk synth

# Deploy
cdk deploy
```

#### 6. Verify Deployment

After deployment, check the outputs:
- S3 Bucket name
- Lambda function name
- Glue database and table names
- EventBridge rule name

### Testing

#### Test Lambda Locally

```bash
# No API key needed!
python test_lambda_local.py
```

#### Test Lambda in AWS

```bash
aws lambda invoke \
  --function-name <WeatherLambdaFunctionName> \
  --payload '{}' \
  response.json

cat response.json
```

#### Verify Data in S3

```bash
aws s3 ls s3://<WeatherDataBucket>/ --recursive
```

#### Query Data in Athena

1. Go to AWS Athena Console
2. Select the Glue database (from CDK outputs)
3. Run queries from `athena_queries.sql`

Example:
```sql
SELECT * FROM weather_db_weatherpipelinestack.weather_data 
ORDER BY timestamp DESC 
LIMIT 10;
```

## CI/CD Setup

### GitHub Secrets Required

Configure these secrets in your GitHub repository:

1. `AWS_ACCESS_KEY_ID` - AWS access key
2. `AWS_SECRET_ACCESS_KEY` - AWS secret key
3. `AWS_ACCOUNT_ID` - Your AWS account ID
4. (Optional) `LATITUDE`, `LONGITUDE`, `CITY`, `COUNTRY_CODE` - Location coordinates

### Workflow Features

- **Lint**: Code quality checks
- **Synth**: CDK synthesis validation
- **Deploy**: Automatic deployment on push to main

## Architecture Diagram

```
┌─────────────┐
│ Weather API │
└──────┬──────┘
       │
       ▼
┌─────────────────┐     Every 1 min    ┌──────────────┐
│ EventBridge Rule│ ──────────────────► │ Lambda       │
└─────────────────┘                     │ Function     │
                                        └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ S3 Bucket    │
                                        │ (Parquet)    │
                                        └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ Glue Table   │
                                        │ (Catalog)    │
                                        └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ Athena       │
                                        │ (Queries)    │
                                        └──────────────┘
```

## Cost Optimization

- **EventBridge**: Consider changing schedule from 1 minute to 5-15 minutes for cost savings
- **Lambda**: Current configuration (256MB, 30s timeout) is cost-effective
- **S3**: Lifecycle policies can be added to move old data to Glacier
- **Athena**: Query only what you need using partitions

## Troubleshooting

### Lambda Import Errors
- Ensure dependencies are installed: `pip install -r lambda/weather_ingestion/requirements.txt -t lambda/weather_ingestion/`

### S3 Permission Errors
- Verify Lambda has write permissions (automatically granted by CDK)

### Glue Table Not Found in Athena
- Wait a few minutes after deployment for table to be available
- Verify database and table names match

### EventBridge Not Triggering
- Check rule is enabled: `aws events describe-rule --name <rule-name>`
- Verify Lambda permissions

### API Issues
- Open-Meteo is free and doesn't require an API key
- Check coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)
- Verify internet connectivity for API calls

## Files Structure

```
cdk-weather-glue/
├── app.py                          # CDK app entry
├── cdk.json                         # CDK config
├── requirements.txt                 # Dependencies
├── infrastructure/
│   └── stack.py                     # Main CDK stack
├── lambda/
│   └── weather_ingestion/           # Lambda function
├── glue/
│   └── scripts/                     # ETL scripts
├── .github/
│   └── workflows/
│       └── deploy.yml               # CI/CD
├── athena_queries.sql              # Example queries
└── test_lambda_local.py            # Local testing
```

## Next Steps

- Monitor Lambda execution in CloudWatch
- Set up CloudWatch alarms for errors
- Add data quality checks
- Implement data retention policies
- Create dashboards in QuickSight or Grafana

## Troubleshooting

### CDK Bootstrap Issues
If you get errors about CDK bootstrap:
```bash
cdk bootstrap aws://ACCOUNT-ID/REGION
```

### Python Virtual Environment
If you have issues with the virtual environment:
- Make sure you're using Python 3.9 or higher
- Try recreating the venv: `rm -rf venv` (or `rmdir /s venv` on Windows) and run setup again

### AWS Credentials
If you get permission errors:
- Verify credentials: `aws sts get-caller-identity`
- Check IAM permissions for CDK deployment

## Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [Open-Meteo API](https://open-meteo.com/) - Free weather API

## License

This project is for educational purposes.

