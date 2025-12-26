# PowerShell Deployment script for Serverless SPA CDK Project
# This script builds and deploys the frontend to AWS S3 + CloudFront

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting deployment process..." -ForegroundColor Blue

# Check if CDK is installed
try {
    $cdkVersion = cdk --version 2>&1
    Write-Host "✓ CDK found: $cdkVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ CDK CLI not found. Please install it: npm install -g aws-cdk" -ForegroundColor Red
    exit 1
}

# Check if AWS credentials are configured
try {
    aws sts get-caller-identity | Out-Null
    Write-Host "✓ AWS credentials configured" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS credentials not configured. Please run: aws configure" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Building frontend assets..." -ForegroundColor Blue

# Ensure frontend directory exists
if (-not (Test-Path "frontend")) {
    Write-Host "❌ Frontend directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "☁️  Synthesizing CDK stack..." -ForegroundColor Blue
cdk synth

Write-Host "📤 Deploying to AWS..." -ForegroundColor Blue
cdk deploy --require-approval never

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Check the CloudFront URL in the outputs above." -ForegroundColor Green

