# Systemd Memory Leak Monitoring Services

## Overview
This document describes the systemd services created for monitoring memory leaks and system health.

## Services Created

### 1. Zombie Process Cleanup
- **Service**: `zombie-cleanup.service`
- **Timer**: `zombie-cleanup.timer`
- **Script**: `cleanup_zombies.sh`
- **Schedule**: Daily at 2:00 AM
- **Purpose**: Clean up zombie processes to prevent resource leaks

### 2. Memory Monitor
- **Service**: `memory-monitor.service`
- **Timer**: `memory-monitor.timer`
- **Script**: `memory_monitor.sh`
- **Schedule**: Every minute
- **Purpose**: Continuously monitor memory usage and swap
- **Alerts**: 
  - Warning at 6GB memory usage
  - Alert at 8GB memory usage
  - Warning at 1GB+ swap usage

### 3. Advanced Memory Analysis
- **Service**: `advanced-memory-monitor.service`
- **Timer**: `advanced-memory-monitor.timer`
- **Script**: `advanced_memory_monitor.sh`
- **Schedule**: Hourly
- **Purpose**: Analyze memory trends and detect leak patterns
- **Features**:
  - Track memory usage history
  - Detect abnormal memory growth
  - Analyze process memory usage
  - Identify potential leak patterns

### 4. System Health Monitor
- **Service**: `system-health-monitor.service`
- **Purpose**: General system health monitoring
- **Script**: `system_health_monitor.sh`

### 5. Daily Tasks
- **Service**: `daily-tasks.service`
- **Purpose**: Execute scheduled daily tasks
- **Script**: `daily_tasks.sh`

## Installation

Run the installation script as root:
```bash
sudo /data/workspace/install_all_monitoring_services.sh
```

## Monitoring Commands

### Check service status
```bash
systemctl status zombie-cleanup.timer
systemctl status memory-monitor.timer
systemctl status advanced-memory-monitor.timer
systemctl status system-health-monitor.service
```

### View logs
```bash
# Zombie cleanup logs
journalctl -u zombie-cleanup.service

# Memory monitor logs
journalctl -u memory-monitor.service

# Advanced memory analysis logs
journalctl -u advanced-memory-monitor.service

# All monitoring logs
journalctl -u "zombie-*" -u "memory-*" -u "advanced-*"
```

### List active timers
```bash
systemctl list-timers --all
```

### View memory history
```bash
tail -f /var/log/memory_history.log
```

## Configuration

### Memory thresholds
- **Warning threshold**: 6GB (can be modified in `memory_monitor.sh`)
- **Alert threshold**: 8GB (can be modified in `memory_monitor.sh`)
- **Swap warning**: 1GB (can be modified in `memory_monitor.sh`)

### Log rotation
- Maximum log size: 10MB (can be modified in monitoring scripts)
- Memory history: Last 100 entries (can be modified in `advanced_memory_monitor.sh`)

### Analysis intervals
- Memory monitoring: Every 60 seconds
- Memory analysis: Every hour
- Zombie cleanup: Daily at 2:00 AM

## Troubleshooting

### Common issues
1. **Services not starting**: Check if scripts are executable
2. **Permission denied**: Ensure services run as root
3. **Log file errors**: Check log directory permissions
4. **Timer not triggering**: Verify systemd daemon is reloaded

### Debug commands
```bash
# Test individual scripts
sudo /data/workspace/cleanup_zombies.sh
sudo /data/workspace/memory_monitor.sh &
sudo /data/workspace/advanced_memory_monitor.sh &

# Check systemd logs
journalctl -xe -u "zombie-*" -u "memory-*" -u "advanced-*"

# Test timer manually
systemctl start zombie-cleanup.timer
systemctl start memory-monitor.timer
systemctl start advanced-memory-monitor.timer
```

## Files

### Configuration files
- `/data/workspace/zombie-cleanup.service`
- `/data/workspace/zombie-cleanup.timer`
- `/data/workspace/memory-monitor.service`
- `/data/workspace/memory-monitor.timer`
- `/data/workspace/advanced-memory-monitor.service`
- `/data/workspace/advanced-memory-monitor.timer`
- `/data/workspace/system-health-monitor.service`
- `/data/workspace/daily-tasks.service`

### Installation scripts
- `/data/workspace/install_all_monitoring_services.sh`
- `/data/workspace/install_systemd_service.sh`

### Monitoring scripts
- `/data/workspace/cleanup_zombies.sh`
- `/data/workspace/memory_monitor.sh`
- `/data/workspace/advanced_memory_monitor.sh`
- `/data/workspace/system_health_monitor.sh`
- `/data/workspace/daily_tasks.sh`

### Log files
- `/var/log/zombie_cleanup.log`
- `/var/log/memory_monitor.log`
- `/var/log/memory_analysis.log`
- `/var/log/memory_history.log`

## Maintenance

### Restart services
```bash
sudo systemctl restart zombie-cleanup.timer
sudo systemctl restart memory-monitor.timer
sudo systemctl restart advanced-memory-monitor.timer
```

### Stop services
```bash
sudo systemctl stop zombie-cleanup.timer
sudo systemctl stop memory-monitor.timer
sudo systemctl stop advanced-memory-monitor.timer
```

### Disable services
```bash
sudo systemctl disable zombie-cleanup.timer
sudo systemctl disable memory-monitor.timer
sudo systemctl disable advanced-memory-monitor.timer
```

### Clean up old logs
```bash
sudo find /var/log -name "*memory*" -o -name "*zombie*" -mtime +30 -delete
```

## Security Notes

- All services run as root for system-level monitoring
- Log files are readable by root only by default
- Scripts include proper error handling
- Services are configured with appropriate restart policies