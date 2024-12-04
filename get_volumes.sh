#!/bin/bash

# Output file
OUTPUT_FILE="volumes.csv"

# Fetch volumes and format output
aws ec2 describe-volumes --query 'Volumes[*]' --output json | \
jq -r '.[] | [
    .VolumeId,
    .Size,
    (.Iops // 0),
    (.Throughput // 0),
    (try (.Attachments[0].InstanceId) // "N/A"),
    (try (.Attachments[0].Device) // "N/A"),
    (try (.Tags[] | select(.Key == "Name") | .Value) // "N/A")
] | @csv' >> $OUTPUT_FILE

echo "Volume details with Name tag, attachment device, and instance ID have been exported to $OUTPUT_FILE."
