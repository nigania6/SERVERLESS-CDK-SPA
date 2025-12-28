#!/bin/bash
echo "========================================"
echo "Dependency Check for Weather Pipeline"
echo "========================================"
echo ""

echo "[1/7] Checking Python..."
if command -v python3 &> /dev/null; then
    python3 --version
    echo "OK: Python installed"
else
    echo "ERROR: Python not found"
fi
echo ""

echo "[2/7] Checking Node.js..."
if command -v node &> /dev/null; then
    node --version
    echo "OK: Node.js installed"
else
    echo "ERROR: Node.js not found"
fi
echo ""

echo "[3/7] Checking AWS CLI..."
if command -v aws &> /dev/null; then
    aws --version
    echo "OK: AWS CLI installed"
else
    echo "ERROR: AWS CLI not found"
fi
echo ""

echo "[4/7] Checking AWS Credentials..."
if aws sts get-caller-identity &> /dev/null; then
    echo "OK: AWS credentials configured"
    aws sts get-caller-identity
else
    echo "ERROR: AWS credentials not configured"
fi
echo ""

echo "[5/7] Checking Virtual Environment..."
if [ -d "venv" ]; then
    echo "OK: Virtual environment exists"
    source venv/bin/activate
    echo "Checking main dependencies..."
    
    if pip show aws-cdk-lib &> /dev/null; then
        echo "OK: aws-cdk-lib installed"
    else
        echo "ERROR: aws-cdk-lib not installed"
    fi
    
    if pip show constructs &> /dev/null; then
        echo "OK: constructs installed"
    else
        echo "ERROR: constructs not installed"
    fi
    
    if pip show boto3 &> /dev/null; then
        echo "OK: boto3 installed"
    else
        echo "ERROR: boto3 not installed"
    fi
    
    if pip show pandas &> /dev/null; then
        echo "OK: pandas installed"
    else
        echo "ERROR: pandas not installed"
    fi
    
    if pip show pyarrow &> /dev/null; then
        echo "OK: pyarrow installed"
    else
        echo "ERROR: pyarrow not installed"
    fi
    
    if pip show requests &> /dev/null; then
        echo "OK: requests installed"
    else
        echo "ERROR: requests not installed"
    fi
else
    echo "ERROR: Virtual environment not found. Run ./setup.sh first."
fi
echo ""

echo "[6/7] Checking Lambda Dependencies..."
if [ -d "lambda/weather_ingestion/boto3" ]; then
    echo "OK: Lambda boto3 installed"
else
    echo "WARNING: Lambda boto3 not installed. Run: pip install -r lambda/weather_ingestion/requirements.txt -t lambda/weather_ingestion/"
fi

if [ -d "lambda/weather_ingestion/requests" ]; then
    echo "OK: Lambda requests installed"
else
    echo "WARNING: Lambda requests not installed"
fi

if [ -d "lambda/weather_ingestion/pandas" ]; then
    echo "OK: Lambda pandas installed"
else
    echo "WARNING: Lambda pandas not installed"
fi

if [ -d "lambda/weather_ingestion/pyarrow" ]; then
    echo "OK: Lambda pyarrow installed"
else
    echo "WARNING: Lambda pyarrow not installed"
fi
echo ""

echo "[7/7] Checking CDK..."
if command -v cdk &> /dev/null; then
    cdk --version
    echo "OK: CDK installed"
else
    echo "ERROR: CDK not found"
fi
echo ""

echo "[BONUS] Checking Environment Variables..."
if [ -n "$WEATHER_API_KEY" ]; then
    echo "OK: WEATHER_API_KEY is set"
else
    echo "WARNING: WEATHER_API_KEY not set"
fi
echo ""

echo "========================================"
echo "Dependency Check Complete"
echo "========================================"