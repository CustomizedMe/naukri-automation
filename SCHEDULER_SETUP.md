# Naukri Automation Scheduler Setup

Your Naukri automation script is now set up to run automatically every morning at 8:00 AM! 🎉

## What's Been Set Up

### ✅ **Automated Scheduling**
- **Cron Job**: Runs daily at 8:00 AM
- **Shell Script**: `run_naukri_automation.sh` handles execution
- **Logging**: All runs are logged with timestamps
- **Error Handling**: Proper error reporting and cleanup

### ✅ **Management Tools**
- **Management Script**: `manage_automation.sh` for easy control
- **Status Checking**: Monitor automation health
- **Log Viewing**: Check recent automation runs
- **Manual Testing**: Run automation on demand

## How to Use

### **Check Status**
```bash
./manage_automation.sh status
```
Shows if automation is active, log files, and system health.

### **Run Now (Manual)**
```bash
./manage_automation.sh start
```
Runs the automation immediately instead of waiting for 8 AM.

### **View Recent Logs**
```bash
./manage_automation.sh logs
```
Shows the last few automation runs and their results.

### **Test the Setup**
```bash
./manage_automation.sh test
```
Runs a complete test to ensure everything works.

### **Stop Automation**
```bash
./manage_automation.sh stop
```
Removes the scheduled automation (stops running at 8 AM).

### **Restart Automation**
```bash
./manage_automation.sh restart
```
Restarts the scheduled automation.

## File Structure

```
/Users/mac/Desktop/Naukri/
├── main.py                          # Main automation script
├── utility.py                       # Automation functions
├── .env                            # Your credentials
├── run_naukri_automation.sh        # Scheduler wrapper
├── manage_automation.sh            # Management tool
├── logs/                           # Automation logs
│   └── naukri_automation_YYYYMMDD.log
└── venv/                          # Python virtual environment
```

## Log Files

- **Location**: `logs/naukri_automation_YYYYMMDD.log`
- **Content**: Full automation run details with timestamps
- **Retention**: Automatically keeps last 30 days of logs
- **Format**: Timestamped entries with emoji indicators

## What Happens at 8 AM

1. **8:00:00** - Cron job triggers the automation
2. **8:00:01** - Shell script starts and logs the beginning
3. **8:00:02** - Virtual environment is activated
4. **8:00:03** - Python script runs the automation
5. **8:00:30** - Automation completes and logs results
6. **8:00:31** - Log file is updated with success/failure

## Troubleshooting

### **Automation Not Running**
```bash
./manage_automation.sh status
```
Check if cron job is active and all files exist.

### **Check Recent Runs**
```bash
./manage_automation.sh logs
```
See what happened in recent automation attempts.

### **Test Everything**
```bash
./manage_automation.sh test
```
Run a complete test to identify any issues.

### **Manual Run**
```bash
./manage_automation.sh start
```
Run automation immediately to test without waiting.

## Security Notes

- ✅ **Credentials**: Stored securely in `.env` file
- ✅ **Logs**: No sensitive data logged (passwords masked)
- ✅ **Permissions**: Scripts have proper executable permissions
- ✅ **Isolation**: Runs in virtual environment

## Customization

### **Change Schedule**
To run at a different time, edit the cron job:
```bash
crontab -e
```
Change `0 8 * * *` to your desired time (format: minute hour day month weekday).

### **Change Login Method**
Edit `.env` file and change `LOGIN_METHOD`:
- `google` - Uses Google OAuth
- `email_password` - Uses direct login
- `otp` - Uses phone OTP

## Success Indicators

When automation runs successfully, you'll see:
- ✅ Chrome starts successfully
- ✅ Login completes
- ✅ Profile page loads
- ✅ Resume uploads successfully
- ✅ Script finishes cleanly

## Your Automation is Ready! 🚀

The system will now automatically refresh your Naukri profile every morning at 8:00 AM. You can monitor it using the management script and check logs anytime.

**Next Steps:**
1. Let it run automatically tomorrow at 8 AM
2. Check logs with `./manage_automation.sh logs`
3. Monitor status with `./manage_automation.sh status`

Happy job hunting! 🎯
