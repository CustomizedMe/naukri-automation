#!/bin/bash

# GitHub Actions Setup Script for Naukri Automation
# This script helps you set up GitHub Actions for your automation

echo "🚀 Setting up GitHub Actions for Naukri Automation"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: Check if git is initialized
print_step "Checking Git repository..."
if [ ! -d ".git" ]; then
    print_warning "Git repository not found. Initializing..."
    git init
    print_success "Git repository initialized"
else
    print_success "Git repository already exists"
fi

# Step 2: Create .gitignore
print_step "Creating .gitignore..."
cat > .gitignore << EOF
# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
env/
ENV/

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# macOS
.DS_Store

# Chrome driver
chromedriver
chromedriver.exe

# Resume files (keep private)
*.pdf
resume/
EOF
print_success ".gitignore created"

# Step 3: Copy requirements file
print_step "Setting up requirements..."
cp requirements-github.txt requirements.txt
print_success "Requirements file ready"

# Step 4: Create README
print_step "Creating README..."
cat > README.md << 'EOF'
# Naukri Profile Automation

Automatically refreshes your Naukri.com profile daily at 8:00 AM IST using GitHub Actions.

## Features

- 🕐 **Daily Automation**: Runs automatically every morning at 8:00 AM IST
- 🔐 **Multiple Login Methods**: Google OAuth, Email/Password, or OTP
- 📝 **Complete Logging**: All runs are logged with detailed results
- ☁️ **Cloud-Based**: Runs on GitHub Actions (24/7 reliability)
- 🔒 **Secure**: Credentials stored as GitHub Secrets

## Setup

1. **Fork this repository** to your GitHub account
2. **Upload your resume** to the repository (name it `resume.pdf`)
3. **Configure secrets** in your GitHub repository settings:
   - `LOGIN_METHOD`: `google`, `email_password`, or `otp`
   - `NAUKRI_EMAIL`: Your Naukri email
   - `NAUKRI_PASSWORD`: Your Naukri password
   - `GOOGLE_EMAIL`: Your Google email (if using Google login)
   - `PHONE_NUMBER`: Your phone number (if using OTP)

## How It Works

1. **GitHub Actions** triggers daily at 8:00 AM IST
2. **Sets up environment** with Python and Chrome
3. **Runs automation** to refresh your Naukri profile
4. **Logs results** and uploads artifacts
5. **Notifies** on success or failure

## Manual Trigger

You can also trigger the automation manually:
1. Go to **Actions** tab in your repository
2. Select **Naukri Profile Automation**
3. Click **Run workflow**

## Security

- All credentials are stored as GitHub Secrets
- Resume file is kept private in your repository
- No sensitive data is logged

## Monitoring

Check the **Actions** tab to see:
- ✅ Successful runs
- ❌ Failed runs with error details
- 📊 Run logs and artifacts

---

**Your job search automation is now running in the cloud! 🚀**
EOF
print_success "README created"

# Step 5: Instructions
echo ""
print_success "GitHub Actions setup complete!"
echo ""
print_step "Next steps:"
echo "1. 📁 Upload your resume as 'resume.pdf' to the repository"
echo "2. 🔐 Add secrets to your GitHub repository:"
echo "   - LOGIN_METHOD (google/email_password/otp)"
echo "   - NAUKRI_EMAIL (your email)"
echo "   - NAUKRI_PASSWORD (your password)"
echo "   - GOOGLE_EMAIL (if using Google login)"
echo "   - PHONE_NUMBER (if using OTP)"
echo "3. 🚀 Push to GitHub and enable Actions"
echo ""
print_warning "Remember to:"
echo "- Keep your resume file private"
echo "- Never commit .env file"
echo "- Test the workflow manually first"
echo ""
print_success "Ready to push to GitHub! 🎉"
