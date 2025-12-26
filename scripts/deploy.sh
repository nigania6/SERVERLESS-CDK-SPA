#!/bin/bash

# Deployment script for Serverless SPA CDK Project
# This script builds and deploys the frontend to AWS S3 + CloudFront

set -e  # Exit on error

echo "🚀 Starting deployment process..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if CDK is installed
if ! command -v cdk &> /dev/null; then
    echo "❌ CDK CLI not found. Please install it: npm install -g aws-cdk"
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run: aws configure"
    exit 1
fi

echo -e "${BLUE}📦 Building frontend assets...${NC}"

# Ensure frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Note: In production, you might want to minify/optimize assets here
# For now, we'll use the assets as-is

echo -e "${BLUE}☁️  Synthesizing CDK stack...${NC}"
cdk synth

echo -e "${BLUE}📤 Deploying to AWS...${NC}"
cdk deploy --require-approval never

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Check the CloudFront URL in the outputs above.${NC}"

