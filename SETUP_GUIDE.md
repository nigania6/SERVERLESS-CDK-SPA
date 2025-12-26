# Setup Guide - Complete Project Setup Instructions

This guide will walk you through setting up the entire project from scratch.

## 📋 Prerequisites Installation

### 1. Install Python 3.9+

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. Check "Add Python to PATH"
4. Verify installation:
   ```bash
   python --version
   ```

**Linux/Mac:**
```bash
# Check if Python 3 is installed
python3 --version

# If not installed (Ubuntu/Debian):
sudo apt update
sudo apt install python3 python3-pip python3-venv

# If not installed (Mac):
brew install python3
```

### 2. Install Node.js 18+

**Windows:**
1. Download from [nodejs.org](https://nodejs.org/)
2. Run installer
3. Verify installation:
   ```bash
   node --version
   npm --version
   ```

**Linux/Mac:**
```bash
# Using Node Version Manager (nvm) - Recommended
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Or download from nodejs.org
```

### 3. Install AWS CLI

**Windows:**
```bash
# Using MSI installer (recommended)
# Download from: https://awscli.amazonaws.com/AWSCLIV2.msi

# Or using pip
pip install awscli
```

**Linux/Mac:**
```bash
# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Mac
brew install awscli
```

**Verify:**
```bash
aws --version
```

### 4. Install AWS CDK CLI

```bash
npm install -g aws-cdk
```

**Verify:**
```bash
cdk --version
```

### 5. Configure AWS Credentials

```bash
aws configure
```

You'll need:
- **AWS Access Key ID**: Get from AWS Console → IAM → Users → Your User → Security credentials
- **AWS Secret Access Key**: Same location (only shown once)
- **Default region**: e.g., `us-east-1`, `eu-west-1`
- **Default output format**: `json`

**Verify:**
```bash
aws sts get-caller-identity
```

## 🚀 Project Setup

### Step 1: Navigate to Project Directory

```bash
cd D:\python-learning\Serverless-SPA-CDK
```

### Step 2: Create Python Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify CDK Setup

```bash
cdk --version
cdk synth
```

The `cdk synth` command should generate CloudFormation templates in the `cdk.out` directory.

## 🧪 Local Testing

### Test Frontend Locally

1. **Start Local Server:**
   ```bash
   cd frontend
   python -m http.server 8000
   ```

2. **Open Browser:**
   ```
   http://localhost:8000
   ```

3. **Test Navigation:**
   - Click each tab: About, Projects, Interiors, Contact
   - Verify smooth scrolling
   - Test on mobile (resize browser)

4. **Verify Functionality:**
   - Check browser console for errors (F12)
   - Test contact form validation
   - Verify responsive design

See [LOCAL_TESTING.md](LOCAL_TESTING.md) for detailed testing instructions.

## ☁️ AWS Deployment

### Step 1: Bootstrap CDK (First Time Only)

```bash
cdk bootstrap
```

This sets up S3 buckets and IAM roles for CDK in your AWS account.

### Step 2: Review Deployment Plan

```bash
cdk diff
```

This shows what resources will be created/changed.

### Step 3: Deploy to AWS

**Option A - Using CDK Directly:**
```bash
cdk deploy
```

**Option B - Using Deployment Script:**

**Windows:**
```powershell
.\scripts\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

**Python (Cross-platform):**
```bash
python scripts/deploy.py
```

### Step 4: Get CloudFront URL

After deployment, CDK will output:
- **CloudFrontURL**: Your website URL (e.g., `https://d1234567890.cloudfront.net`)
- **DistributionId**: CloudFront distribution ID
- **BucketName**: S3 bucket name

**Note:** CloudFront distribution may take 10-15 minutes to fully deploy.

### Step 5: Verify Deployment

1. Open CloudFront URL in browser
2. Test all sections
3. Verify HTTPS works
4. Test direct URL access (e.g., `https://d1234567890.cloudfront.net#projects`)
5. Check browser console for errors

## 🔄 GitHub Integration

### Step 1: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Serverless SPA CDK project"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `Serverless-SPA-CDK`
3. Don't initialize with README (we already have one)

### Step 3: Connect and Push

```bash
git remote add origin https://github.com/YOUR_USERNAME/Serverless-SPA-CDK.git
git branch -M main
git push -u origin main
```

### Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: `Settings` → `Secrets and variables` → `Actions`
3. Click `New repository secret`
4. Add the following secrets:

   - **Name:** `AWS_ACCESS_KEY_ID`
     **Value:** Your AWS access key

   - **Name:** `AWS_SECRET_ACCESS_KEY`
     **Value:** Your AWS secret key

   - **Name:** `AWS_ACCOUNT_ID`
     **Value:** Your AWS account ID (12 digits)

5. Update `.github/workflows/deploy.yml` if your region is different from `us-east-1`

### Step 5: Test GitHub Actions

1. Make a small change to `frontend/index.html`
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test GitHub Actions deployment"
   git push
   ```
3. Go to `Actions` tab in GitHub
4. Watch the deployment workflow run
5. Verify your website updates

## 📝 Project Structure Overview

```
Serverless-SPA-CDK/
├── frontend/              # Frontend SPA
│   ├── index.html        # Main HTML
│   ├── css/
│   │   └── style.css     # Styles
│   ├── js/
│   │   └── app.js        # JavaScript
│   └── images/           # Image assets
├── serverless_spa_cdk/   # CDK Stack
│   ├── __init__.py
│   └── serverless_spa_cdk_stack.py
├── scripts/              # Deployment scripts
│   ├── deploy.sh
│   ├── deploy.ps1
│   └── deploy.py
├── .github/
│   └── workflows/
│       └── deploy.yml    # CI/CD Pipeline
├── app.py                # CDK App Entry
├── cdk.json              # CDK Config
├── requirements.txt      # Python Deps
├── TODO.md               # Project Roadmap
├── README.md             # Main Documentation
├── LOCAL_TESTING.md      # Testing Guide
└── SETUP_GUIDE.md       # This file
```

## 🐛 Troubleshooting

### Issue: CDK Command Not Found
**Solution:**
```bash
npm install -g aws-cdk
# Verify installation
cdk --version
```

### Issue: Python Module Not Found
**Solution:**
```bash
# Ensure virtual environment is activated
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: AWS Credentials Error
**Solution:**
```bash
# Verify credentials
aws sts get-caller-identity

# If it fails, reconfigure
aws configure
```

### Issue: CDK Bootstrap Fails
**Solution:**
```bash
# Bootstrap explicitly for your account/region
cdk bootstrap aws://ACCOUNT-ID/REGION

# Replace ACCOUNT-ID with your 12-digit AWS account ID
# Replace REGION with your region (e.g., us-east-1)
```

### Issue: Deployment Fails
**Solution:**
- Check AWS Console → CloudFormation for error details
- Verify you have necessary permissions (S3, CloudFront, IAM)
- Check CDK version: `cdk --version` (should be 2.x)

### Issue: GitHub Actions Fails
**Solution:**
- Verify all GitHub Secrets are set correctly
- Check workflow logs in GitHub Actions tab
- Ensure AWS credentials are valid
- Verify account ID and region are correct

## ✅ Verification Checklist

After setup, verify:

- [ ] Python 3.9+ installed and working
- [ ] Node.js 18+ installed and working
- [ ] AWS CLI configured and working
- [ ] CDK CLI installed and working
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Local frontend works (`http://localhost:8000`)
- [ ] CDK synth works (`cdk synth`)
- [ ] CDK bootstrap completed
- [ ] AWS deployment successful
- [ ] CloudFront URL accessible
- [ ] GitHub repository created
- [ ] GitHub Actions workflow runs successfully

## 📚 Next Steps

1. ✅ Complete local testing (see [LOCAL_TESTING.md](LOCAL_TESTING.md))
2. ✅ Deploy to AWS (see above)
3. ✅ Verify deployment works
4. ✅ Set up GitHub repository and push code
5. ✅ Configure GitHub Actions
6. ✅ Test automated deployment

## 🎉 Success!

If everything works:
- Your SPA is running locally ✅
- Your SPA is deployed to AWS ✅
- GitHub Actions is set up ✅

You can now:
- Make changes locally
- Test locally
- Push to GitHub
- Automatic deployment will happen!

---

**Need Help?** Check the [README.md](README.md) or [TODO.md](TODO.md) for more information.

