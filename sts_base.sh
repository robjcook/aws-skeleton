assume_role_output=$(aws sts assume-role \
    --role-arn "arn:aws:iam::123456789012:role/YourRoleName" \
    --role-session-name "YourSessionName" \
    --output json)

aws_access_key_id=$(echo $assume_role_output | jq -r '.Credentials.AccessKeyId')
aws_secret_access_key=$(echo $assume_role_output | jq -r '.Credentials.SecretAccessKey')
aws_session_token=$(echo $assume_role_output | jq -r '.Credentials.SessionToken')

export AWS_ACCESS_KEY_ID="$aws_access_key_id"
export AWS_SECRET_ACCESS_KEY="$aws_secret_access_key"
export AWS_SESSION_TOKEN="$aws_session_token"
