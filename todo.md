# Weather Data Pipeline - Project Todo & Structure

## Project Overview
Serverless data pipeline that ingests weather data from free API, stores in S3 as Parquet, processes with Glue, and enables querying via Athena - all without using Glue Crawler.

---

## Pipeline Architecture

```
Weather API → Lambda (Every 1 min) → S3 (Parquet) → Glue Table → Athena Queries
                                                      ↓
                                              Glue ETL Job (Optional)
```

---

## Execution Stages

### ✅ Stage 1: Project Setup & Dependencies
- [ ] Initialize AWS CDK project
- [ ] Set up Python virtual environment
- [ ] Install dependencies (boto3, aws-cdk-lib, pandas, pyarrow, requests)
- [ ] Configure CDK bootstrap
- [ ] Set up AWS credentials


---

### ✅ Stage 2: Weather API Integration
- [ ] Create Lambda function for weather data fetching
- [ ] Implement API call logic (OpenWeatherMap or similar)
- [ ] Convert JSON response to Parquet format
- [ ] Upload Parquet file to S3 with partitioning
- [ ] Test Lambda function locally

---

### ✅ Stage 3: EventBridge Schedule
- [ ] Create EventBridge rule (cron: every 1 minute)
- [ ] Configure Lambda trigger
- [ ] Set up IAM permissions for EventBridge → Lambda
- [ ] Test scheduled execution


---

### ✅ Stage 4: S3 Bucket Structure
- [ ] Create S3 bucket for weather data
- [ ] Configure bucket with partitioning structure (year/month/day/hour)
- [ ] Set up bucket policies and encryption
- [ ] Configure lifecycle policies (optional)


---

### ✅ Stage 5: Glue Catalog & Table (No Crawler)
- [ ] Create Glue database
- [ ] Define Glue table schema programmatically
- [ ] Map table to S3 location
- [ ] Configure Parquet SerDe
- [ ] Set up partition columns
- [ ] Verify table creation


---

### ✅ Stage 6: Glue ETL Job (Optional)
- [ ] Create Glue ETL job script
- [ ] Configure job parameters
- [ ] Set up job triggers (optional)
- [ ] Test data transformations


---

### ✅ Stage 7: Athena Setup
- [ ] Verify Glue table is accessible in Athena
- [ ] Test sample queries
- [ ] Create example queries for common use cases
- [ ] Document query patterns


---

### ✅ Stage 8: CI/CD with GitHub Actions
- [ ] Create GitHub Actions workflow file
- [ ] Configure AWS credentials as secrets
- [ ] Set up CDK deployment steps
- [ ] Add testing/validation steps
- [ ] Configure workflow triggers (push to main)
- [ ] Test deployment pipeline


---

### ✅ Stage 9: Testing & Documentation
- [ ] End-to-end pipeline testing
- [ ] Verify data flow (API → S3 → Athena)
- [ ] Create comprehensive README.md
- [ ] Document setup instructions
- [ ] Add troubleshooting guide
- [ ] Create architecture diagram


---

## Project Structure

```
cdk-weather-glue/
│
├── app.py                          # CDK app entry point
├── cdk.json                        # CDK configuration
├── requirements.txt                # Python dependencies
├── setup.sh / setup.bat           # Environment setup scripts
├── todo.md                         # This file
├── README.md                       # Project documentation
│
├── infrastructure/
│   └── stack.py                    # Main CDK stack (S3, Lambda, Glue, EventBridge)
│
├── lambda/
│   └── weather_ingestion/
│       ├── lambda_function.py      # Weather API Lambda handler
│       ├── requirements.txt        # Lambda-specific dependencies
│       └── utils.py                # Helper functions (Parquet conversion, etc.)
│
├── glue/
│   └── scripts/
│       └── transform_weather.py    # Glue ETL transformation script (optional)
│
└── .github/
    └── workflows/
        └── deploy.yml              # GitHub Actions CI/CD pipeline
```

---

## Key Components

### 1. **Lambda Function** (`lambda/weather_ingestion/`)
   - Fetches weather data from free API
   - Converts JSON to Parquet format
   - Uploads to S3 with partitioning (year/month/day/hour)

### 2. **EventBridge Rule**
   - Scheduled trigger (every 1 minute)
   - Invokes Lambda function

### 3. **S3 Bucket**
   - Stores Parquet files
   - Partitioned structure: `s3://bucket/year=YYYY/month=MM/day=DD/hour=HH/`

### 4. **Glue Database & Table**
   - Database: `weather_db`
   - Table: `weather_data` (schema defined in CDK, no crawler)
   - Location: S3 bucket path
   - Format: Parquet

### 5. **Athena**
   - Query interface for weather data
   - Uses Glue table metadata

### 6. **AWS CDK**
   - Infrastructure as Code
   - All resources defined programmatically

### 7. **GitHub Actions**
   - Automated deployment
   - CDK synth and deploy on push

---

## Total Estimated Time

**For Beginners:** 6-10 hours
- Learning AWS concepts: 2-3 hours
- Implementation: 4-6 hours
- Debugging & Testing: 1-2 hours

**For Experienced Developers:** 3-5 hours

---

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Python 3.9+ installed
- Node.js (for CDK)
- GitHub repository
- Weather API key (e.g., OpenWeatherMap)

---

## Next Steps

1. Start with Stage 1: Project Setup
2. Follow stages sequentially
3. Test each stage before moving to next
4. Document any issues encountered

---

## Notes

- **No Glue Crawler**: Table schema is defined programmatically in CDK
- **Partitioning**: S3 structure enables efficient Athena queries
- **Cost Optimization**: Consider adjusting EventBridge schedule frequency for cost savings
- **Error Handling**: Implement retry logic and error notifications

