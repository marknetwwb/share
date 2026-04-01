#!/bin/bash
# Enhanced systemd service installation script for zombie cleanup

SERVICE_FILE="/data/workspace/zombie-cleanup.service"
TIMER_FILE="/data/workspace/zombie-cleanup.timer"
SCRIPT_FILE="/data/workspace/cleanup_zombies.sh"
SYSTEMD_DIR="/etc/systemd/system"
LOG_DIR="/var/log"

echo "🔧 Installing systemd units for zombie cleanup..."

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ This script needs to be run as root. Please use sudo."
    exit 1
fi

# Create log directory if it doesn't exist
if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory: $LOG_DIR"
    mkdir -p "$LOG_DIR"
fi

# Ensure cleanup script is executable
echo "Ensuring cleanup script is executable..."
chmod +x "$SCRIPT_FILE"

# Copy service and timer files to systemd directory
echo "📁 Copying service file to $SYSTEMD_DIR..."
cp "$SERVICE_FILE" "$SYSTEMD_DIR/"

echo "📁 Copying timer file to $SYSTEMD_DIR..."
cp "$TIMER_FILE" "$SYSTEMD_DIR/"

# Reload systemd to recognize new units
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

# Remove old cron job if it exists
echo "🗑️ Removing old cron job if it exists..."
crontab -l 2>/dev/null | grep -v "/data/workspace/cleanup_zombies.sh" | crontab -

# Enable the timer
echo "⚡ Enabling zombie-cleanup.timer..."
systemctl enable zombie-cleanup.timer

# Start the timer
echo "▶️ Starting zombie-cleanup.timer..."
systemctl start zombie-cleanup.timer

# Verify the installation
echo "✅ Verifying installation..."
echo "Timer status:"
systemctl status zombie-cleanup.timer --no-pager -n 15

echo ""
echo "Next run time:"
systemctl list-timers --all --no-pager -n 5

echo ""
echo "📊 Systemd timer details:"
systemctl show zombie-cleanup.timer --no-pager

echo ""
echo "✅ Systemd installation completed successfully!"
echo "🎯 The zombie cleanup will run daily at 2:00 AM (±5 minutes random delay)"
echo ""
echo "🔧 Useful commands:"
echo "   systemctl status zombie-cleanup.timer     # Check timer status"
echo "   systemctl status zombie-cleanup.service   # Check service status"
echo "   journalctl -u zombie-cleanup.service      # View service logs"
echo "   systemctl list-timers                    # List all active timers"
echo "   systemctl disable zombie-cleanup.timer   # Disable timer"
echo "   systemctl stop zombie-cleanup.timer       # Stop timer"
echo ""
echo "📝 Log location: /var/log/zombie_cleanup.log"
echo "📋 Service configuration: /etc/systemd/system/zombie-cleanup.service"
echo "📋 Timer configuration: /etc/systemd/system/zombie-cleanup.timer"