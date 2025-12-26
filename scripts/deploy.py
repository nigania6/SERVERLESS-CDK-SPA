#!/usr/bin/env python3
"""
Deployment script for Serverless SPA CDK Project
This script builds and deploys the frontend to AWS S3 + CloudFront
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(e.stderr)
        sys.exit(1)

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check CDK
    try:
        subprocess.run(["cdk", "--version"], check=True, capture_output=True)
        print("✅ CDK CLI found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ CDK CLI not found. Please install it: npm install -g aws-cdk")
        sys.exit(1)
    
    # Check AWS CLI
    try:
        subprocess.run(["aws", "sts", "get-caller-identity"], check=True, capture_output=True)
        print("✅ AWS credentials configured")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ AWS credentials not configured. Please run: aws configure")
        sys.exit(1)

def main():
    """Main deployment function"""
    print("🚀 Starting deployment process...\n")
    
    # Check requirements
    check_requirements()
    print()
    
    # Check if frontend directory exists
    if not Path("frontend").exists():
        print("❌ Frontend directory not found!")
        sys.exit(1)
    
    # Synthesize CDK stack
    run_command("cdk synth", "Synthesizing CDK stack")
    print()
    
    # Deploy to AWS
    run_command("cdk deploy --require-approval never", "Deploying to AWS")
    print()
    
    print("✅ Deployment completed successfully!")
    print("🌐 Check the CloudFront URL in the outputs above.")

if __name__ == "__main__":
    main()

