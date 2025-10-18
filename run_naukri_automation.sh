#!/bin/bash

# Naukri Automation Scheduler Script
# This script runs the Naukri automation every morning at 8 AM

# Set the script directory
SCRIPT_DIR="/Users/mac/Desktop/Naukri"
LOG_DIR="$SCRIPT_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Set log file with date
LOG_FILE="$LOG_DIR/naukri_automation_$(date +%Y%m%d).log"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Start logging
log_message "🚀 Starting Naukri automation..."

# Change to script directory
cd "$SCRIPT_DIR" || {
    log_message "❌ Failed to change to script directory: $SCRIPT_DIR"
    exit 1
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    log_message "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and run the script
log_message "🔧 Activating virtual environment..."
source venv/bin/activate || {
    log_message "❌ Failed to activate virtual environment"
    exit 1
}

# Check if main.py exists
if [ ! -f "main.py" ]; then
    log_message "❌ main.py not found"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    log_message "❌ .env file not found. Please configure your credentials."
    exit 1
fi

# Run the Python script
log_message "🐍 Running Naukri automation script..."
python main.py 2>&1 | tee -a "$LOG_FILE"

# Capture exit code
EXIT_CODE=${PIPESTATUS[0]}

# Log completion
if [ $EXIT_CODE -eq 0 ]; then
    log_message "✅ Naukri automation completed successfully"
else
    log_message "❌ Naukri automation failed with exit code: $EXIT_CODE"
fi

# Deactivate virtual environment
deactivate

# Log script completion
log_message "🏁 Automation script finished"

# Clean up old log files (keep last 30 days)
find "$LOG_DIR" -name "naukri_automation_*.log" -mtime +30 -delete 2>/dev/null

exit $EXIT_CODE
