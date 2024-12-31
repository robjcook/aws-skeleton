#!/bin/bash

# Fetch an IMDSv2 token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)

# Check if token retrieval was successful
if [ -z "$TOKEN" ]; then
    echo "Failed to retrieve metadata token. Ensure IMDS is enabled."
    exit 1
fi

# Fetch instance ID using the token
INSTANCE_ID=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/instance-id)

# Validate the instance ID
if [ -z "$INSTANCE_ID" ]; then
    echo "Failed to retrieve instance ID. Check network and metadata service configuration."
    exit 1
fi

# Extract the last 4 characters of the instance ID
INSTANCE_ID_SUFFIX=${INSTANCE_ID: -4}

# Fetch the Name tag of the instance using AWS CLI
INSTANCE_NAME=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=Name" \
    --query "Tags[0].Value" --output text)

# Validate the Name tag
if [ -z "$INSTANCE_NAME" ]; then
    echo "Failed to retrieve Name tag. Check AWS CLI configuration and permissions."
    exit 1
fi

# Concatenate the Name tag and the last 4 characters of the Instance ID
NEW_HOSTNAME="${INSTANCE_NAME}-${INSTANCE_ID_SUFFIX}"

# Set the new hostname
sudo hostnamectl set-hostname "$NEW_HOSTNAME"
