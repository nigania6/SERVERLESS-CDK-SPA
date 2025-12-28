#!/bin/bash
# Setup script for Linux/Mac

echo "===================================="
echo "Weather Pipeline - Stage 1 Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "[1/5] Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Upgrading pip..."
pip install --upgrade pip

echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[5/5] Checking AWS CLI..."
if ! command -v aws &> /dev/null; then
    echo "WARNING: AWS CLI is not installed"
    echo "Please install AWS CLI and configure credentials"
else
    echo "AWS CLI is installed"
fi

echo ""
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo ""
echo "Next steps:"
echo "1. Make sure AWS credentials are configured: aws configure"
echo "2. Bootstrap CDK (first time only): cdk bootstrap"
echo "3. Deploy the stack: cdk deploy"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""

