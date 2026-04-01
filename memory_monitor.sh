#!/bin/bash
# Memory leak monitoring script

LOG_FILE="/var/log/memory_monitor.log"
ALERT_THRESHOLD_MB=8192  # 8GB threshold for alerts
WARNING_THRESHOLD_MB=6144  # 6GB threshold for warnings
SAMPLE_INTERVAL=60       # Check every 60 seconds
MAX_LOG_SIZE=10485760    # 10MB max log size

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Function to get memory usage in MB
get_memory_usage() {
    free -m | grep '^Mem:' | awk '{print $3}'  # Used memory
}

# Function to get swap usage in MB
get_swap_usage() {
    free -m | grep '^Swap:' | awk '{print $3}'  # Used swap
}

# Function to get process memory usage
get_process_memory() {
    ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -11
}

# Function to log with timestamp
log_with_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to check if log file needs rotation
rotate_log_if_needed() {
    if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -gt $MAX_LOG_SIZE ]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
        log_with_timestamp "Log rotated - size exceeded ${MAX_LOG_SIZE} bytes"
    fi
}

# Main monitoring loop
log_with_timestamp "=== Memory leak monitoring started ==="

while true; do
    rotate_log_if_needed
    
    MEMORY_MB=$(get_memory_usage)
    SWAP_MB=$(get_swap_usage)
    
    # Log memory usage
    log_with_timestamp "Memory Usage: ${MEMORY_MB}MB / ${SWAP_MB}MB swap"
    
    # Check for alerts
    if [ "$MEMORY_MB" -gt "$ALERT_THRESHOLD_MB" ]; then
        log_with_timestamp "⚠️ ALERT: Memory usage above threshold (${MEMORY_MB}MB > ${ALERT_THRESHOLD_MB}MB)"
        log_with_timestamp "Top memory consuming processes:"
        get_process_memory >> "$LOG_FILE"
        log_with_timestamp ""
    elif [ "$MEMORY_MB" -gt "$WARNING_THRESHOLD_MB" ]; then
        log_with_timestamp "⚠️ WARNING: Memory usage approaching threshold (${MEMORY_MB}MB > ${WARNING_THRESHOLD_MB}MB)"
        log_with_timestamp "Top memory consuming processes:"
        get_process_memory >> "$LOG_FILE"
        log_with_timestamp ""
    fi
    
    # Check for abnormal swap usage
    if [ "$SWAP_MB" -gt 1024 ]; then  # More than 1GB swap usage
        log_with_timestamp "⚠️ WARNING: High swap usage detected (${SWAP_MB}MB)"
        log_with_timestamp ""
    fi
    
    # Wait for next check
    sleep "$SAMPLE_INTERVAL"
done