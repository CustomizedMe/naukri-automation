#!/bin/bash

# Naukri Automation Management Script
# This script helps you manage the scheduled automation

SCRIPT_DIR="/Users/mac/Desktop/Naukri"
LOG_DIR="$SCRIPT_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Function to show help
show_help() {
    echo "Naukri Automation Management Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  status     - Show automation status"
    echo "  start      - Start automation now"
    echo "  stop       - Stop scheduled automation"
    echo "  restart    - Restart scheduled automation"
    echo "  logs       - Show recent logs"
    echo "  test       - Test the automation script"
    echo "  help       - Show this help message"
    echo ""
}

# Function to check automation status
check_status() {
    print_info "Checking automation status..."
    
    # Check if cron job exists
    if crontab -l 2>/dev/null | grep -q "run_naukri_automation.sh"; then
        print_status "Scheduled automation is ACTIVE"
        echo "Schedule: Daily at 8:00 AM"
        echo "Script: $SCRIPT_DIR/run_naukri_automation.sh"
    else
        print_warning "Scheduled automation is NOT ACTIVE"
    fi
    
    # Check if log directory exists
    if [ -d "$LOG_DIR" ]; then
        print_status "Log directory exists: $LOG_DIR"
        LOG_COUNT=$(ls -1 "$LOG_DIR"/*.log 2>/dev/null | wc -l)
        echo "Log files: $LOG_COUNT"
    else
        print_warning "Log directory not found: $LOG_DIR"
    fi
    
    # Check if virtual environment exists
    if [ -d "$SCRIPT_DIR/venv" ]; then
        print_status "Virtual environment exists"
    else
        print_error "Virtual environment not found"
    fi
    
    # Check if .env file exists
    if [ -f "$SCRIPT_DIR/.env" ]; then
        print_status "Environment configuration exists"
    else
        print_error "Environment configuration (.env) not found"
    fi
}

# Function to start automation now
start_now() {
    print_info "Starting Naukri automation now..."
    cd "$SCRIPT_DIR" || {
        print_error "Failed to change to script directory"
        exit 1
    }
    ./run_naukri_automation.sh
}

# Function to stop scheduled automation
stop_automation() {
    print_info "Stopping scheduled automation..."
    crontab -r 2>/dev/null
    print_status "Scheduled automation stopped"
}

# Function to restart scheduled automation
restart_automation() {
    print_info "Restarting scheduled automation..."
    stop_automation
    echo "0 8 * * * $SCRIPT_DIR/run_naukri_automation.sh" | crontab -
    print_status "Scheduled automation restarted (Daily at 8:00 AM)"
}

# Function to show recent logs
show_logs() {
    print_info "Recent automation logs:"
    echo ""
    
    if [ -d "$LOG_DIR" ]; then
        # Show last 3 log files
        ls -t "$LOG_DIR"/*.log 2>/dev/null | head -3 | while read logfile; do
            echo "📄 $(basename "$logfile"):"
            echo "----------------------------------------"
            tail -20 "$logfile"
            echo ""
        done
    else
        print_warning "No log directory found"
    fi
}

# Function to test automation
test_automation() {
    print_info "Testing automation script..."
    cd "$SCRIPT_DIR" || {
        print_error "Failed to change to script directory"
        exit 1
    }
    
    # Check if all required files exist
    if [ ! -f "main.py" ]; then
        print_error "main.py not found"
        exit 1
    fi
    
    if [ ! -f ".env" ]; then
        print_error ".env file not found"
        exit 1
    fi
    
    if [ ! -d "venv" ]; then
        print_error "Virtual environment not found"
        exit 1
    fi
    
    print_status "All required files found"
    print_info "Running test..."
    ./run_naukri_automation.sh
}

# Main script logic
case "$1" in
    "status")
        check_status
        ;;
    "start")
        start_now
        ;;
    "stop")
        stop_automation
        ;;
    "restart")
        restart_automation
        ;;
    "logs")
        show_logs
        ;;
    "test")
        test_automation
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
