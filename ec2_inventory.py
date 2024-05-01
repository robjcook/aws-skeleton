import boto3
import pandas as pd

# Initialize boto3 client
ec2 = boto3.client('ec2')

# Get list of instances
response = ec2.describe_instances()

# Parse instance data
instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_info = {
            'InstanceId': instance['InstanceId'],
            'InstanceType': instance['InstanceType'],
            'State': instance['State']['Name'],
            'PrivateIpAddress': instance.get('PrivateIpAddress', ''),
            'PublicIpAddress': instance.get('PublicIpAddress', ''),
            # Add more attributes as needed
        }
        instances.append(instance_info)

# Convert to DataFrame
df = pd.DataFrame(instances)

# Export to Excel
df.to_excel('ec2_instances.xlsx', index=False)
