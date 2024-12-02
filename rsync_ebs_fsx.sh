#!/bin/bash

# Variables
SOURCE_DIR="/path/to/ebs/volume"  # Replace with your EBS volume mount path
DEST_DIR="/path/to/fsx/mount"     # Replace with your FSx mount path
LOG_FILE="/var/log/ebs_to_fsx.log"
METRICS_INTERVAL=10               # Interval to log server metrics (seconds)

# Function to log server metrics
log_metrics() {
    echo "=== Server Metrics at $(date) ===" >> "$LOG_FILE"
    echo "CPU Usage:" >> "$LOG_FILE"
    top -b -n1 | grep "Cpu(s)" | awk '{print $2 + $4"%"}' >> "$LOG_FILE"
    echo "Memory Usage:" >> "$LOG_FILE"
    free -h >> "$LOG_FILE"
    echo "Disk Usage:" >> "$LOG_FILE"
    df -h >> "$LOG_FILE"
    echo "==================================" >> "$LOG_FILE"
}

# Function to monitor rsync progress
monitor_rsync() {
    echo "Starting rsync from $SOURCE_DIR to $DEST_DIR at $(date)" >> "$LOG_FILE"
    rsync -avh --progress "$SOURCE_DIR" "$DEST_DIR" | while IFS= read -r line; do
        echo "$(date): $line" >> "$LOG_FILE"
    done
    if [[ $? -eq 0 ]]; then
        echo "rsync completed successfully at $(date)" >> "$LOG_FILE"
    else
        echo "rsync encountered an error at $(date)" >> "$LOG_FILE"
    fi
}

# Function to run server metrics logging in the background
start_metrics_logging() {
    while true; do
        log_metrics
        sleep "$METRICS_INTERVAL"
    done
}

# Run metrics logging in the background
start_metrics_logging &

# Start rsync and monitor progress
monitor_rsync

# Kill background metrics logging when rsync is done
pkill -P $$

echo "Script completed at $(date)" >> "$LOG_FILE"
