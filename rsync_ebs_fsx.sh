#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <source> <destination>"
  exit 1
fi

# Get source and destination from script arguments
SOURCE="$1"
DESTINATION="$2"

# Log file location
LOGFILE="rsync_progress.log"
PROGRESS_LOG="rsync_progress_temp.log"

# Record start time
START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
START_EPOCH=$(date +%s)

# Print start time to log
echo "----------------------------------------" >> "$LOGFILE"
echo "Rsync started at: $START_TIME" >> "$LOGFILE"
echo "Source: $SOURCE" >> "$LOGFILE"
echo "Destination: $DESTINATION" >> "$LOGFILE"

# Start rsync in the background, redirecting its progress output to a temporary file
rsync -avh --info=progress2 "$SOURCE" "$DESTINATION" > "$PROGRESS_LOG" 2>&1 &
RSYNC_PID=$!

# Periodically log progress every 5 minutes
while kill -0 "$RSYNC_PID" 2> /dev/null; do
  echo "Progress at $(date +"%Y-%m-%d %H:%M:%S"):" >> "$LOGFILE"
  tail -n 1 "$PROGRESS_LOG" >> "$LOGFILE"
  echo "----------------------------------------" >> "$LOGFILE"
  sleep 300  # Wait 5 minutes
done

# Wait for rsync to complete
wait "$RSYNC_PID"

# Record end time
END_TIME=$(date +"%Y-%m-%d %H:%M:%S")
END_EPOCH=$(date +%s)

# Calculate elapsed time
ELAPSED_SECONDS=$((END_EPOCH - START_EPOCH))
ELAPSED=$(printf "%02d:%02d:%02d" $((ELAPSED_SECONDS / 3600)) $(( (ELAPSED_SECONDS / 60) % 60 )) $((ELAPSED_SECONDS % 60)))

# Print end time and elapsed time to log
echo "Rsync completed at: $END_TIME" >> "$LOGFILE"
echo "Time elapsed: $ELAPSED" >> "$LOGFILE"
echo "----------------------------------------" >> "$LOGFILE"

# Clean up temporary progress log
rm -f "$PROGRESS_LOG"

# Inform the user where the log is saved
echo "Rsync completed. See log in $LOGFILE."
