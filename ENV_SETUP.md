# Environment Variables Setup Guide

This document explains how to configure the Naukri automation script using environment variables.

## Required Environment Variables

### 1. Login Method Configuration
```bash
LOGIN_METHOD=google  # Options: google, email_password, otp
```

### 2. For Google Login
```bash
LOGIN_METHOD=google
GOOGLE_EMAIL=your-email@gmail.com
```

**Note**: For Google login, the script will:
- Use your existing Chrome session if available
- Automatically select your Google account
- Handle OAuth authentication

### 3. For Email/Password Login
```bash
LOGIN_METHOD=email_password
NAUKRI_EMAIL=your-email@example.com
NAUKRI_PASSWORD=your-password
```

### 4. For OTP Login
```bash
LOGIN_METHOD=otp
PHONE_NUMBER=+91XXXXXXXXXX
```

**Note**: For OTP login, you'll need to manually enter the OTP when prompted.

## Complete .env File Example

```bash
# Login Configuration
LOGIN_METHOD=google  # Change this to: google, email_password, or otp

# For Google Login (uses existing Chrome session)
GOOGLE_EMAIL=prakharbhatnagar5337@gmail.com

# For Email/Password Login
NAUKRI_EMAIL=prakharbhatnagar5337@gmail.com
NAUKRI_PASSWORD=your-password-here

# For OTP Login
PHONE_NUMBER=+91XXXXXXXXXX
```

## How to Use

1. **Copy the example above** to your `.env` file
2. **Set LOGIN_METHOD** to your preferred method:
   - `google` - Uses Google OAuth (recommended if you're logged into Google)
   - `email_password` - Uses direct Naukri login
   - `otp` - Uses phone number and OTP
3. **Fill in the required credentials** for your chosen method
4. **Run the script**: `python main.py`

## Login Method Details

### Google Login (Recommended)
- **Pros**: Automatic, uses existing Chrome session, secure
- **Cons**: Requires Google account, may need 2FA setup
- **Best for**: Users already logged into Google Chrome

### Email/Password Login
- **Pros**: Direct, no external dependencies
- **Cons**: Less secure, may be blocked by 2FA
- **Best for**: Users with simple Naukri accounts

### OTP Login
- **Pros**: Secure, no password storage
- **Cons**: Requires manual OTP entry, needs phone
- **Best for**: Users who prefer phone-based authentication

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for email/password login
- Keep your phone accessible for OTP login
- Consider using Google login for better security

## Troubleshooting

### Google Login Issues
- Make sure you're logged into Google Chrome
- Check if 2FA is enabled on your Google account
- Try clearing Chrome cache and cookies

### Email/Password Issues
- Verify your Naukri credentials
- Check if your account has 2FA enabled
- Try logging in manually first

### OTP Issues
- Ensure your phone number is correct
- Check if you have network connectivity
- Wait for the OTP to arrive (can take 1-2 minutes)
