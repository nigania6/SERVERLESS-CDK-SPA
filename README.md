# Serverless SPA CDK Project

A single-page application (SPA) for Architectural Designing Services, built with AWS CDK, S3, and CloudFront.

## 🌟 Features

- **Single Page Application** with smooth navigation
- **Responsive Design** for mobile, tablet, and desktop
- **AWS Serverless Infrastructure** using CDK
- **Sections**: About, Projects, Interiors, Contact
- **Modern UI/UX** with smooth animations
- **Automated Deployment** via GitHub Actions

## 📋 Prerequisites

- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- AWS Account with appropriate permissions
- AWS CLI configured ([Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html))
- CDK CLI installed globally: `npm install -g aws-cdk`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Serverless-SPA-CDK
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Local Testing

Before deploying to AWS, test the application locally:

```bash
# Navigate to frontend directory
cd frontend

# Start local web server
# Option 1: Python HTTP Server
python -m http.server 8000

# Option 2: Node.js http-server (if installed)
npx http-server -p 8000

# Open browser and navigate to:
# http://localhost:8000
```

**Verify the following:**
- ✅ All navigation tabs work (About, Projects, Interiors, Contact)
- ✅ No console errors
- ✅ Responsive design works on different screen sizes
- ✅ Contact form validation works
- ✅ All assets load correctly

### 4. Configure AWS

```bash
# Configure AWS credentials
aws configure

# Bootstrap CDK (first time only)
cdk bootstrap
```

### 5. Deploy to AWS

```bash
# Review what will be created
cdk diff

# Deploy the stack
cdk deploy

# Or use the deployment script:
# Windows PowerShell:
.\scripts\deploy.ps1

# Linux/Mac:
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# Python (cross-platform):
python scripts/deploy.py
```

After deployment, you'll see the CloudFront URL in the outputs. It may take 10-15 minutes for the CloudFront distribution to be fully deployed.

### 6. Verify Deployment

1. Access the CloudFront URL from the CDK outputs
2. Test all sections of the website
3. Verify HTTPS is working
4. Test direct URL access (SPA routing)
5. Check browser console for errors

## 📁 Project Structure

```
Serverless-SPA-CDK/
├── frontend/                 # Frontend SPA files
│   ├── index.html           # Main HTML file
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   ├── js/
│   │   └── app.js           # JavaScript application logic
│   └── images/              # Image assets
├── serverless_spa_cdk/      # CDK stack definition
│   ├── __init__.py
│   └── serverless_spa_cdk_stack.py
├── scripts/                 # Deployment scripts
│   ├── deploy.sh           # Bash deployment script
│   ├── deploy.ps1          # PowerShell deployment script
│   └── deploy.py           # Python deployment script
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions CI/CD
├── app.py                   # CDK app entry point
├── cdk.json                 # CDK configuration
├── requirements.txt         # Python dependencies
├── TODO.md                  # Project roadmap and tasks
└── README.md               # This file
```

## 🔧 Configuration

### CDK Stack Configuration

Edit `serverless_spa_cdk/serverless_spa_cdk_stack.py` to customize:
- S3 bucket name
- CloudFront distribution settings
- Cache policies
- Error page handling

### Frontend Customization

- **Content**: Edit `frontend/index.html`
- **Styling**: Modify `frontend/css/style.css`
- **Behavior**: Update `frontend/js/app.js`

## 🌐 GitHub Actions CI/CD

### Setup GitHub Secrets

To enable automated deployments, add these secrets to your GitHub repository:

1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `AWS_ACCOUNT_ID`: Your AWS account ID
   - `AWS_REGION`: Your AWS region (or update in workflow file)

### Workflow Triggers

The deployment workflow triggers on:
- Push to `main` or `master` branch
- Manual workflow dispatch

## 📝 Development Workflow

1. **Local Development**
   - Make changes to frontend files
   - Test locally using `python -m http.server 8000`
   - Verify all functionality works

2. **Local Deployment**
   - Run `cdk deploy` to test AWS deployment
   - Verify CloudFront URL works correctly

3. **GitHub Deployment**
   - Commit and push changes to GitHub
   - GitHub Actions will automatically deploy
   - Monitor deployment in Actions tab

## 🛠️ Troubleshooting

### CDK Bootstrap Issues

```bash
# Bootstrap CDK for your account and region
cdk bootstrap aws://ACCOUNT-ID/REGION
```

### CloudFront Not Updating

- CloudFront distributions take time to deploy (10-15 minutes)
- The CDK stack automatically invalidates cache on deployment
- You can manually invalidate: `aws cloudfront create-invalidation --distribution-id DIST_ID --paths "/*"`

### SPA Routing (404 Errors)

The stack is configured to redirect 403/404 errors to `index.html` for SPA routing. If you see 404 errors:
- Check CloudFront error page configuration in the CDK stack
- Verify error responses are set correctly

### Assets Not Loading

- Ensure all paths in HTML/CSS/JS are relative (not absolute)
- Check S3 bucket policy and Origin Access Control (OAC) configuration
- Verify CloudFront distribution is in "Deployed" status

## 🔒 Security Best Practices

- Never commit AWS credentials to git
- Use IAM roles with least privilege
- Enable S3 bucket encryption
- Use HTTPS only (CloudFront default)
- Regularly update dependencies

## 💰 Cost Considerations

This project uses AWS free tier eligible services:
- **S3**: 5GB storage, 20,000 GET requests/month (first year)
- **CloudFront**: 1TB data transfer, 10,000,000 HTTP/HTTPS requests/month (first year)

After free tier, costs are typically:
- S3: ~$0.023 per GB/month
- CloudFront: ~$0.085 per GB (first 10TB)

## 📚 Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [S3 Documentation](https://docs.aws.amazon.com/s3/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally and verify deployment
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
- Check the [TODO.md](TODO.md) for troubleshooting guide
- Review AWS CloudFormation stack events in AWS Console
- Check CloudWatch logs for detailed error messages

---

**Built with ❤️ using AWS CDK**

