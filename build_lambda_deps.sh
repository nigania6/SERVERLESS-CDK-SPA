#!/bin/bash
set -e
echo "Building Lambda dependencies for Python 3.11..."

cd lambda/weather_ingestion

# Clean existing dependencies
rm -rf boto3 botocore certifi charset_normalizer dateutil idna jmespath \
       numpy pandas pyarrow pytz requests s3transfer tzdata urllib3 six.py \
       bin numpy.libs __pycache__ *.pyc *.pyo *.pyd *.so *-*.dist-info *-*.egg-info 2>/dev/null || true

# Try Docker first, fallback to local Python 3.11
if command -v docker &> /dev/null && docker ps &> /dev/null; then
    echo "Using Docker to build dependencies..."
    docker run --rm -v "$(pwd)":/var/task \
        public.ecr.aws/lambda/python:3.11 \
        /bin/bash -c "pip install --no-cache-dir -r requirements.txt -t ."
else
    echo "Docker not available, using local Python 3.11..."
    if ! command -v python3.11 &> /dev/null; then
        echo "❌ ERROR: Python 3.11 not found!"
        echo "Install it with: sudo apt install -y python3.11 python3.11-venv python3.11-dev"
        echo "Or use deadsnakes PPA: sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update && sudo apt install -y python3.11"
        exit 1
    fi
    python3.11 -m pip install --upgrade pip --user 2>/dev/null || true
    python3.11 -m pip install --no-cache-dir -r requirements.txt -t .
fi

echo "✅ Dependencies built successfully!"
