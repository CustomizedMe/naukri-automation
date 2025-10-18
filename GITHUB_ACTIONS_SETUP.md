# GitHub Actions Setup Guide

Your Naukri automation is now ready for GitHub Actions! This will run your automation 24/7 in the cloud, completely independent of your laptop.

## 🚀 **What's Been Set Up**

### ✅ **GitHub Actions Workflow**
- **File**: `.github/workflows/naukri-automation.yml`
- **Schedule**: Daily at 8:00 AM IST (2:30 AM UTC)
- **Manual Trigger**: Available for testing
- **Logging**: Complete logs with artifacts

### ✅ **Repository Structure**
- **Requirements**: Clean Python dependencies
- **Gitignore**: Protects sensitive files
- **README**: Complete documentation
- **Workflow**: Automated execution

## 📋 **Step-by-Step Setup**

### **Step 1: Create GitHub Repository**
1. Go to [GitHub.com](https://github.com)
2. Click **"New repository"**
3. Name it: `naukri-automation`
4. Make it **Private** (recommended)
5. Click **"Create repository"**

### **Step 2: Upload Your Resume**
1. In your repository, click **"Add file"** → **"Upload files"**
2. Upload your resume and name it `resume.pdf`
3. Click **"Commit changes"**

### **Step 3: Configure Secrets**
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add these secrets:

```
LOGIN_METHOD = email_password
NAUKRI_EMAIL = your-email@example.com
NAUKRI_PASSWORD = your-password
GOOGLE_EMAIL = your-google-email@gmail.com (if using Google)
PHONE_NUMBER = +91XXXXXXXXXX (if using OTP)
```

### **Step 4: Push Your Code**
```bash
# Add all files
git add .

# Commit changes
git commit -m "Add Naukri automation with GitHub Actions"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/naukri-automation.git

# Push to GitHub
git push -u origin main
```

### **Step 5: Enable Actions**
1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Your automation is now active!

## 🎯 **How It Works**

### **Daily Execution (8:00 AM IST)**
1. **GitHub Actions** automatically triggers
2. **Sets up Ubuntu environment** with Python and Chrome
3. **Installs dependencies** and downloads your resume
4. **Runs automation** to refresh your Naukri profile
5. **Logs results** and uploads artifacts
6. **Notifies** on success or failure

### **Manual Testing**
1. Go to **Actions** tab
2. Select **"Naukri Profile Automation"**
3. Click **"Run workflow"**
4. Click **"Run workflow"** button
5. Watch it execute in real-time!

## 📊 **Monitoring Your Automation**

### **Check Status**
- **Actions tab**: See all runs (success/failure)
- **Green checkmark**: ✅ Successful run
- **Red X**: ❌ Failed run
- **Yellow circle**: ⏳ Currently running

### **View Logs**
1. Click on any run
2. Click on **"naukri-automation"** job
3. Expand steps to see detailed logs
4. Download artifacts for complete logs

### **Success Indicators**
```
✅ Naukri automation completed successfully!
🕐 Time: 2025-10-19 02:30:15
📊 Run ID: 1234567890
```

## 🔧 **Configuration Options**

### **Change Schedule**
Edit `.github/workflows/naukri-automation.yml`:
```yaml
schedule:
  - cron: '30 2 * * *'  # 8:00 AM IST
  - cron: '0 9 * * *'   # 9:00 AM IST
  - cron: '0 12 * * *'  # 12:00 PM IST
```

### **Change Login Method**
Update the `LOGIN_METHOD` secret:
- `google` - Google OAuth
- `email_password` - Direct login
- `otp` - Phone OTP

## 🛡️ **Security Features**

### ✅ **Protected Credentials**
- All passwords stored as GitHub Secrets
- Never visible in logs or code
- Encrypted at rest

### ✅ **Private Repository**
- Resume file kept private
- No public access to your data
- Complete control over visibility

### ✅ **Secure Execution**
- Runs in isolated GitHub environment
- No access to your local machine
- Automatic cleanup after execution

## 🎉 **Benefits of GitHub Actions**

### **✅ 24/7 Reliability**
- Runs even when your laptop is off
- No dependency on your computer
- Professional cloud infrastructure

### **✅ Free Usage**
- 2,000 minutes/month free
- Your automation uses ~2 minutes/day
- Plenty of free usage available

### **✅ Complete Logging**
- Every run is logged
- Easy to debug issues
- Historical data available

### **✅ Easy Management**
- Web interface for monitoring
- Manual triggers for testing
- Simple configuration changes

## 🚀 **Your Automation is Now Cloud-Powered!**

Once set up, your Naukri profile will be automatically refreshed every morning at 8:00 AM IST, completely independent of your laptop. You can monitor it from anywhere using GitHub's web interface.

**Happy job hunting! 🎯**
