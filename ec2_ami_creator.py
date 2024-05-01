import boto3
import json

def lambda_handler(event, context):
    # Extract relevant information from the event
    ami_id = event['detail']['responseElements']['imageId']
    creator = event['detail']['userIdentity']['arn']  # Assuming ARN indicates the IAM entity
    
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')
    
    # Add tags to the newly created AMI
    tags = [{'Key': 'CreatedBy', 'Value': creator}]
    ec2.create_tags(Resources=[ami_id], Tags=tags)
    
    return {
        'statusCode': 200,
        'body': json.dumps('AMI tagging successful')
    }
