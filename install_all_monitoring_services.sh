#!/bin/bash
# Comprehensive systemd services installation for system monitoring

echo "🔧 Installing comprehensive system monitoring systemd services..."

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ This script needs to be run as root. Please use sudo."
    exit 1
fi

# Create log directories
LOG_DIRS=("/var/log" "/var/log/systemd")
for dir in "${LOG_DIRS[@]}"; do
    mkdir -p "$dir"
done

# List of services to install
SERVICES=(
    "zombie-cleanup.service"
    "zombie-cleanup.timer"
    "memory-monitor.service"
    "memory-monitor.timer"
    "advanced-memory-monitor.service"
    "advanced-memory-monitor.timer"
    "system-health-monitor.service"
    "daily-tasks.service"
)

# Copy all service and timer files
for service in "${SERVICES[@]}"; do
    if [ -f "/data/workspace/$service" ]; then
        echo "📁 Installing $service..."
        cp "/data/workspace/$service" "/etc/systemd/system/"
    else
        echo "⚠️ Warning: $service not found in /data/workspace/"
    fi
done

# Make all scripts executable
SCRIPTS=(
    "/data/workspace/cleanup_zombies.sh"
    "/data/workspace/memory_monitor.sh"
    "/data/workspace/advanced_memory_monitor.sh"
    "/data/workspace/system_health_monitor.sh"
    "/data/workspace/daily_tasks.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo "✅ Made executable: $script"
    fi
done

# Reload systemd daemon
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

# Enable and start services
echo "⚡ Enabling and starting timer services..."
systemctl enable zombie-cleanup.timer
systemctl start zombie-cleanup.timer

systemctl enable memory-monitor.timer
systemctl start memory-monitor.timer

systemctl enable advanced-memory-monitor.timer
systemctl start advanced-memory-monitor.timer

echo "⚡ Enabling system services..."
systemctl enable system-health-monitor.service
systemctl start system-health-monitor.service

systemctl enable daily-tasks.service

# Verify installation
echo ""
echo "✅ Installation completed! Verifying services..."
echo ""
echo "📊 Active timers:"
systemctl list-timers --all --no-pager -n 10
echo ""
echo "📊 Active services:"
systemctl list-units --type=service --state=active --no-pager -n 10 | grep -E "(zombie|memory|health|daily)"
echo ""
echo "🔧 Service status details:"
echo "Zombie cleanup timer:"
systemctl status zombie-cleanup.timer --no-pager -n 5
echo ""
echo "Memory monitor timer:"
systemctl status memory-monitor.timer --no-pager -n 5
echo ""
echo "Advanced memory monitor timer:"
systemctl status advanced-memory-monitor.timer --no-pager -n 5
echo ""
echo "📝 Log files:"
echo "   - Zombie cleanup: /var/log/zombie_cleanup.log"
echo "   - Memory monitor: /var/log/memory_monitor.log"
echo "   - Memory analysis: /var/log/memory_analysis.log"
echo "   - Memory history: /var/log/memory_history.log"
echo ""
echo "🔧 Useful commands:"
echo "   systemctl list-timers                    # List all active timers"
echo "   systemctl list-units --type=service    # List all services"
echo "   journalctl -u zombie-cleanup.timer       # View zombie cleanup logs"
echo "   journalctl -u memory-monitor.timer      # View memory monitor logs"
echo "   journalctl -u advanced-memory-monitor.timer # View advanced analysis logs"
echo "   systemctl status <service>.timer        # Check specific timer status"
echo ""
echo "🎯 Monitoring Summary:"
echo "   • Zombie processes: Cleaned daily at 2:00 AM"
echo "   • Memory usage: Monitored every minute"
echo "   • Memory analysis: Detailed analysis every hour"
echo "   • System health: Continuous monitoring"
echo "   • Daily tasks: Executed on schedule"
echo ""
echo "✅ All systemd services installed and configured successfully!"