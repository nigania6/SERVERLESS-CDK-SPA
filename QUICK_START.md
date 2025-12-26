# Quick Start Guide

## 🚀 Fast Track Setup

### 1. Install Prerequisites (One Time)
```bash
# Install Python 3.9+, Node.js 18+, AWS CLI, CDK
# See SETUP_GUIDE.md for detailed instructions

# Install CDK globally
npm install -g aws-cdk

# Configure AWS
aws configure
```

### 2. Setup Project (First Time)
```bash
# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Test Locally
```bash
cd frontend
python -m http.server 8000
# Open: http://localhost:8000
```

### 4. Deploy to AWS
```bash
# Bootstrap (first time only)
cdk bootstrap

# Deploy
cdk deploy

# Or use script:
# Windows: .\scripts\deploy.ps1
# Linux/Mac: ./scripts/deploy.sh
```

### 5. Setup GitHub CI/CD
1. Push code to GitHub
2. Add secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`
3. Push to `main` branch → Auto-deploy! 🎉

## 📝 Common Commands

```bash
# Local testing
cd frontend && python -m http.server 8000

# CDK commands
cdk synth          # Generate CloudFormation template
cdk deploy         # Deploy to AWS
cdk diff           # See what will change
cdk destroy        # Delete all resources

# Git commands
git add .
git commit -m "Your message"
git push origin main
```

## 🆘 Need Help?

- **Full Setup**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Local Testing**: See [LOCAL_TESTING.md](LOCAL_TESTING.md)
- **Project Roadmap**: See [TODO.md](TODO.md)
- **Main Documentation**: See [README.md](README.md)

