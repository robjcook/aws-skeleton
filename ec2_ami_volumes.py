import boto3

# Initialize Boto3 client
ec2 = boto3.client('ec2')

# Specify the AMI ID
ami_id = 'your_ami_id_here'

# Specify the tag key and value to filter snapshots
tag_key = 'your_tag_key'
tag_value = 'your_tag_value'

# Get the list of snapshots associated with the AMI
response = ec2.describe_images(ImageIds=[ami_id])
snapshots = response['Images'][0]['BlockDeviceMappings']

# Iterate through the snapshots and create volumes
for snapshot in snapshots:
    snapshot_id = snapshot['Ebs']['SnapshotId']
    snapshot_tags_response = ec2.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [snapshot_id]
            },
            {
                'Name': 'key',
                'Values': [tag_key]
            },
            {
                'Name': 'value',
                'Values': [tag_value]
            }
        ]
    )
    
    # Check if the snapshot has the specified tag
    if snapshot_tags_response['Tags']:
        volume_size = snapshot['Ebs']['VolumeSize']
        availability_zone = snapshot['Ebs']['DeleteOnTermination']
        
        # Create volume from snapshot
        volume_response = ec2.create_volume(
            SnapshotId=snapshot_id,
            AvailabilityZone=availability_zone,
            VolumeType='gp2',  # Specify the volume type as per your requirement
            Encrypted=False,   # Specify whether the volume should be encrypted
            Size=volume_size   # Specify the size of the volume
        )
        
        # Print volume information
        print("Volume created with ID:", volume_response['VolumeId'])
