# Testing Guide

This guide provides comprehensive testing instructions for the Weather Data Pipeline.

## Table of Contents

1. [Pre-Deployment Testing](#pre-deployment-testing)
2. [Post-Deployment Testing](#post-deployment-testing)
3. [End-to-End Testing](#end-to-end-testing)
4. [Performance Testing](#performance-testing)
5. [Error Handling Testing](#error-handling-testing)

## Pre-Deployment Testing

### 1. Local Lambda Testing

Test the Lambda function locally before deploying:

```bash
# Set environment variables
export WEATHER_API_KEY=your_api_key
export WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather
export S3_BUCKET=test-bucket
export CITY=London
export COUNTRY_CODE=GB

# Run test
python test_lambda_local.py
```

**Expected Output:**
- Status code: 200
- Message: "Weather data successfully ingested"
- Note: S3 upload will fail locally (expected)

### 2. CDK Synthesis

Validate CDK stack before deployment:

```bash
cdk synth
```

**Check for:**
- No syntax errors
- All resources defined correctly
- Environment variables set

### 3. Code Quality

```bash
# Install linting tools
pip install flake8 pylint

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Post-Deployment Testing

### 1. Verify Resources Created

```bash
# Check stack outputs
aws cloudformation describe-stacks \
  --stack-name WeatherPipelineStack \
  --query 'Stacks[0].Outputs' \
  --output table

# Verify S3 bucket
aws s3 ls | grep weather-data

# Verify Lambda function
aws lambda list-functions | grep WeatherIngestion

# Verify EventBridge rule
aws events list-rules | grep WeatherIngestion

# Verify Glue database
aws glue get-database --name weather_db_weatherpipelinestack

# Verify Glue table
aws glue get-table \
  --database-name weather_db_weatherpipelinestack \
  --name weather_data
```

### 2. Test Lambda Function

#### Manual Invocation

```bash
# Get function name from stack outputs
FUNCTION_NAME=$(aws cloudformation describe-stacks \
  --stack-name WeatherPipelineStack \
  --query 'Stacks[0].Outputs[?OutputKey==`WeatherLambdaFunctionName`].OutputValue' \
  --output text)

# Invoke function
aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --payload '{"city":"London","country_code":"GB"}' \
  response.json

# Check response
cat response.json
```

**Expected Response:**
```json
{
  "statusCode": 200,
  "body": "{\"message\":\"Weather data successfully ingested\",...}"
}
```

#### Check CloudWatch Logs

```bash
aws logs tail /aws/lambda/<function-name> --follow
```

### 3. Verify EventBridge Schedule

# Get the actual rule name from stack outputs
RULE_NAME=$(aws cloudformation describe-stacks \
  --stack-name WeatherPipelineStack \
  --query 'Stacks[0].Outputs[?OutputKey==`EventBridgeRuleName`].OutputValue' \
  --output text)

# Check rule status
aws events describe-rule --name $RULE_NAME

# List recent invocations (check CloudWatch Logs)
aws logs filter-log-events \
  --log-group-name /aws/lambda/<function-name> \
  --start-time $(date -u -d '10 minutes ago' +%s)000

### 4. Verify S3 Data

```bash
# List files in bucket
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name WeatherPipelineStack \
  --query 'Stacks[0].Outputs[?OutputKey==`WeatherDataBucket`].OutputValue' \
  --output text)

aws s3 ls s3://$BUCKET_NAME --recursive

# Check file structure (should have partitions)
aws s3 ls s3://$BUCKET_NAME/year=2024/month=01/day=15/hour=14/
```

**Expected Structure:**
```
year=2024/month=01/day=15/hour=14/london_gb_20240115_143022.parquet
```

### 5. Test Glue Table

```bash
# Verify table exists
aws glue get-table \
  --database-name weather_db_weatherpipelinestack \
  --name weather_data

# Check table schema
aws glue get-table \
  --database-name weather_db_weatherpipelinestack \
  --name weather_data \
  --query 'Table.StorageDescriptor.Columns' \
  --output table
```

### 6. Test Athena Queries

1. Go to AWS Athena Console
2. Select database: `weather_db_weatherpipelinestack`
3. Run test query:

```sql
SELECT COUNT(*) as total_records
FROM weather_data;
```

4. Run partitioned query:

```sql
SELECT 
    year, month, day, hour,
    COUNT(*) as records
FROM weather_data
GROUP BY year, month, day, hour
ORDER BY year DESC, month DESC, day DESC, hour DESC
LIMIT 10;
```

## End-to-End Testing

### Test Complete Pipeline Flow

1. **Trigger Lambda manually** (or wait for EventBridge)
2. **Wait 2-3 minutes** for data to be written
3. **Verify S3 file exists**:
   ```bash
   aws s3 ls s3://$BUCKET_NAME --recursive | tail -5
   ```
4. **Query in Athena**:
   ```sql
   SELECT * FROM weather_data 
   ORDER BY timestamp DESC 
   LIMIT 5;
   ```
5. **Verify data quality**:
   ```sql
   SELECT 
       COUNT(*) as total,
       MIN(timestamp) as earliest,
       MAX(timestamp) as latest,
       AVG(temperature) as avg_temp
   FROM weather_data;
   ```

### Test Multiple Cities

```bash
# Invoke with different city
aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --payload '{"city":"NewYork","country_code":"US"}' \
  response2.json
```

## Performance Testing

### Lambda Performance

```bash
# Check Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=$FUNCTION_NAME \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum
```

**Expected:**
- Duration: < 5 seconds
- Memory: < 256MB
- Errors: 0

### S3 Upload Performance

Monitor S3 metrics in CloudWatch:
- Number of PUT requests
- Data transfer out

### Athena Query Performance

Test query performance:

```sql
-- Simple query (should be fast)
SELECT * FROM weather_data LIMIT 10;

-- Partitioned query (should be efficient)
SELECT * FROM weather_data 
WHERE year = '2024' 
  AND month = '01' 
  AND day = '15';
```

## Error Handling Testing

### 1. Test Invalid API Key

```bash
# Temporarily set invalid key
aws lambda update-function-configuration \
  --function-name $FUNCTION_NAME \
  --environment Variables="{WEATHER_API_KEY=invalid_key,...}"

# Invoke and check for error
aws lambda invoke --function-name $FUNCTION_NAME response.json
cat response.json
```

### 2. Test Invalid City

```bash
aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --payload '{"city":"InvalidCity123","country_code":"XX"}' \
  response.json
```

### 3. Test S3 Permission Issues

Temporarily remove S3 permissions and verify error handling.

### 4. Monitor Error Rate

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=$FUNCTION_NAME \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

## Automated Testing Script

Create a test script:

```bash
#!/bin/bash
# test_pipeline.sh

set -e

echo "Testing Weather Pipeline..."

# Get stack outputs
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name WeatherPipelineStack \
  --query 'Stacks[0].Outputs[?OutputKey==`WeatherDataBucket`].OutputValue' \
  --output text)

FUNCTION_NAME=$(aws cloudformation describe-stacks \
  --stack-name WeatherPipelineStack \
  --query 'Stacks[0].Outputs[?OutputKey==`WeatherLambdaFunctionName`].OutputValue' \
  --output text)

echo "1. Testing Lambda invocation..."
aws lambda invoke --function-name $FUNCTION_NAME response.json
if [ $? -eq 0 ]; then
    echo "✅ Lambda invocation successful"
else
    echo "❌ Lambda invocation failed"
    exit 1
fi

echo "2. Checking S3 bucket..."
if aws s3 ls s3://$BUCKET_NAME/ > /dev/null 2>&1; then
    echo "✅ S3 bucket accessible"
else
    echo "❌ S3 bucket not accessible"
    exit 1
fi

echo "3. Waiting for data ingestion (30 seconds)..."
sleep 30

echo "4. Checking for data files..."
FILE_COUNT=$(aws s3 ls s3://$BUCKET_NAME --recursive | wc -l)
if [ $FILE_COUNT -gt 0 ]; then
    echo "✅ Found $FILE_COUNT files in S3"
else
    echo "⚠️  No files found yet (may need more time)"
fi

echo "Testing complete!"
```

## Test Checklist

- [ ] Lambda function executes successfully
- [ ] Data is written to S3 in correct format
- [ ] S3 files have correct partitioning structure
- [ ] Glue table is accessible in Athena
- [ ] Athena queries return correct results
- [ ] EventBridge triggers Lambda on schedule
- [ ] Error handling works correctly
- [ ] CloudWatch logs are generated
- [ ] Performance metrics are acceptable
- [ ] Multiple cities can be processed

## Troubleshooting Test Failures

### Lambda Fails
- Check CloudWatch logs
- Verify API key is correct
- Check IAM permissions

### No Data in S3
- Verify Lambda executed successfully
- Check S3 bucket permissions
- Verify partition structure

### Athena Queries Fail
- Wait a few minutes after data ingestion
- Verify Glue table schema matches data
- Check partition columns are correct

### EventBridge Not Triggering
- Verify rule is enabled
- Check Lambda permissions
- Review CloudWatch Events logs

