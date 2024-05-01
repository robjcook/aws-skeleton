import boto3

# Create an STS client
sts_client = boto3.client('sts')

# Assume a role
response = sts_client.assume_role(
    RoleArn='arn:aws:iam::123456789012:role/YourRoleName',
    RoleSessionName='YourSessionName'
)

# Extract temporary credentials
credentials = response['Credentials']

# Create a new session with the assumed role credentials
session = boto3.Session(
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

# Now you can use this session to interact with AWS services as the assumed role
