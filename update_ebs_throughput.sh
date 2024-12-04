#!/bin/bash

# Check if required arguments are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <volume_ids_file> <throughput_value>"
  echo "Example: $0 volumes.txt 500"
  exit 1
fi

# Input file containing EBS Volume IDs (one per line)
VOLUME_IDS_FILE="$1"

# Desired throughput value in MiB/s
THROUGHPUT="$2"

# Ensure the file exists
if [ ! -f "$VOLUME_IDS_FILE" ]; then
  echo "Error: File '$VOLUME_IDS_FILE' not found."
  exit 1
fi

# Loop through each volume ID in the file
while IFS= read -r VOLUME_ID; do
  # Skip empty lines
  if [ -z "$VOLUME_ID" ]; then
    continue
  fi
  
  echo "Updating throughput for volume: $VOLUME_ID to $THROUGHPUT MiB/s"
  
  # Update the volume's throughput
  aws ec2 modify-volume \
    --volume-id "$VOLUME_ID" \
    --throughput "$THROUGHPUT"
  
  # Check if the command was successful
  if [ $? -eq 0 ]; then
    echo "Successfully updated throughput for volume: $VOLUME_ID"
  else
    echo "Failed to update throughput for volume: $VOLUME_ID"
  fi
done < "$VOLUME_IDS_FILE"

echo "EBS volume throughput update script completed."
