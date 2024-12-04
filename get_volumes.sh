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
    (try (.Tags[] | select(.Key == "Name") | .Value) // "N/A")
] | @csv' >> $OUTPUT_FILE

echo "Volume details with the Name tag have been exported to $OUTPUT_FILE."
