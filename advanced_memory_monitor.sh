#!/bin/bash
# Advanced memory leak analysis script

LOG_FILE="/var/log/memory_analysis.log"
ANALYSIS_INTERVAL=3600  # Run analysis every hour
MEMORY_HISTORY_FILE="/var/log/memory_history.log"
MAX_HISTORY_SIZE=100     # Keep last 100 entries

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Function to get memory usage
get_memory_stats() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'),$(free -m | grep '^Mem:' | awk '{print $3}'),$(free -m | grep '^Mem:' | awk '{print $2}'),$(free -m | grep '^Swap:' | awk '{print $3}'),$(free -m | grep '^Swap:' | awk '{print $2}')" >> "$MEMORY_HISTORY_FILE"
    
    # Limit history file size
    if [ $(wc -l < "$MEMORY_HISTORY_FILE") -gt $MAX_HISTORY_SIZE ]; then
        tail -n $MAX_HISTORY_SIZE "$MEMORY_HISTORY_FILE" > "${MEMORY_HISTORY_FILE}.tmp" && mv "${MEMORY_HISTORY_FILE}.tmp" "$MEMORY_HISTORY_FILE"
    fi
}

# Function to analyze memory trends
analyze_memory_trends() {
    if [ -f "$MEMORY_HISTORY_FILE" ] && [ $(wc -l < "$MEMORY_HISTORY_FILE") -gt 10 ]; then
        echo "=== Memory Trend Analysis ===" >> "$LOG_FILE"
        
        # Calculate memory usage trend
        CURRENT_MEMORY=$(tail -n 1 "$MEMORY_HISTORY_FILE" | cut -d',' -f2)
        OLDER_MEMORY=$(head -n 1 "$MEMORY_HISTORY_FILE" | cut -d',' -f2)
        MEMORY_DIFF=$((CURRENT_MEMORY - OLDER_MEMORY))
        
        echo "Current memory: ${CURRENT_MEMORY}MB" >> "$LOG_FILE"
        echo "Older memory: ${OLDER_MEMORY}MB" >> "$LOG_FILE"
        echo "Memory difference: ${MEMORY_DIFF}MB" >> "$LOG_FILE"
        
        # Check for memory leak pattern
        if [ "$MEMORY_DIFF" -gt 500 ]; then  # More than 500MB increase
            echo "⚠️ POTENTIAL MEMORY LEAK DETECTED: ${MEMORY_DIFF}MB increase detected" >> "$LOG_FILE"
        fi
        
        # Check for processes with abnormal memory growth
        echo "=== Processes with high memory usage ===" >> "$LOG_FILE"
        ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -10 >> "$LOG_FILE"
        
        echo "=== Zombie processes ===" >> "$LOG_FILE"
        ps aux | grep defunct | grep -v grep >> "$LOG_FILE"
        
        echo "=== Memory analysis completed ===" >> "$LOG_FILE"
    fi
}

# Function to check for memory leaks by comparing over time
check_memory_leaks() {
    # Check if memory usage is consistently increasing
    if [ -f "$MEMORY_HISTORY_FILE" ] && [ $(wc -l < "$MEMORY_HISTORY_FILE") -gt 20 ]; then
        echo "=== Detailed Memory Leak Analysis ===" >> "$LOG_FILE"
        
        # Calculate average memory growth rate
        TOTAL_LINES=$(wc -l < "$MEMORY_HISTORY_FILE")
        SAMPLE_SIZE=10
        
        # Get last 10 samples
        LAST_SAMPLES=$(tail -n $SAMPLE_SIZE "$MEMORY_HISTORY_FILE")
        
        # Check if memory is trending upwards
        INCREASING_COUNT=0
        PREV_MEMORY=0
        
        while read -r line; do
            CURRENT_MEMORY=$(echo "$line" | cut -d',' -f2)
            if [ "$PREV_MEMORY" -gt 0 ] && [ "$CURRENT_MEMORY" -gt "$PREV_MEMORY" ]; then
                INCREASING_COUNT=$((INCREASING_COUNT + 1))
            fi
            PREV_MEMORY=$CURRENT_MEMORY
        done <<< "$LAST_SAMPLES"
        
        echo "Memory samples analyzed: $SAMPLE_SIZE" >> "$LOG_FILE"
        echo "Increasing memory samples: $INCREASING_COUNT" >> "$LOG_FILE"
        
        if [ "$INCREASING_COUNT" -gt 7 ]; then  # 70% of samples show increase
            echo "⚠️ STRONG MEMORY LEAK SIGNAL: $INCREASING_COUNT out of $SAMPLE_SIZE samples show increasing memory usage" >> "$LOG_FILE"
        fi
        
        echo "=== Memory leak analysis completed ===" >> "$LOG_FILE"
    fi
}

# Main monitoring loop
echo "=== Memory leak analysis started ===" >> "$LOG_FILE"

while true; do
    get_memory_stats
    analyze_memory_trends
    check_memory_leaks
    
    # Wait for next analysis
    sleep "$ANALYSIS_INTERVAL"
done