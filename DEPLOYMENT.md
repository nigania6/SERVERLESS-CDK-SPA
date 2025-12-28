# Deployment Guide

## Stage 2 Deployment: Lambda Function with Dependencies

When deploying the Lambda function, CDK needs to package the function code along with its dependencies. Here's how to handle this:

### Option 1: Install Dependencies Before Deployment (Recommended)

Before deploying, install Lambda dependencies in the Lambda directory:

```bash
# From project root
cd lambda/weather_ingestion
pip install -r requirements.txt -t .
cd ../..
```

Then deploy:

```bash
cdk deploy -c weather_api_key=YOUR_API_KEY
```

### Option 2: Use Docker for Lambda Bundling

If you have Docker installed, CDK can automatically bundle dependencies using Docker. This requires no manual steps, but Docker must be running.

The current setup uses `Code.from_asset()` which packages the directory as-is. To enable Docker bundling, you would need to modify `infrastructure/stack.py` to use bundling options.

### Option 3: Create a Lambda Layer (Advanced)

For production, consider creating a Lambda Layer for dependencies to reduce deployment package size and enable reuse.

## Quick Deployment Steps

1. **Set API Key:**
   ```bash
   export WEATHER_API_KEY=your_api_key_here
   ```

2. **Install Lambda Dependencies:**
   ```bash
   pip install -r lambda/weather_ingestion/requirements.txt -t lambda/weather_ingestion/
   ```

3. **Deploy:**
   ```bash
   cdk synth  # Check for errors
   cdk deploy
   ```

4. **Test:**
   ```bash
   # Get function name from CDK output
   aws lambda invoke \
     --function-name <function-name> \
     --payload '{}' \
     response.json
   ```

## Troubleshooting

### Lambda Import Errors

If you see import errors in Lambda logs, ensure dependencies are installed in the Lambda directory before deployment.

### S3 Permission Errors

The Lambda function needs write permissions to the S3 bucket. This is automatically granted by the CDK stack via `weather_bucket.grant_write(weather_lambda)`.

### API Key Not Found

Make sure to set the API key via:
- Environment variable: `export WEATHER_API_KEY=your_key`
- CDK context: `cdk deploy -c weather_api_key=your_key`

