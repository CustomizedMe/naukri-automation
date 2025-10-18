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
