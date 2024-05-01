import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Describe volumes
    volumes = ec2.describe_volumes()['Volumes']
    
    # Backup volumes
    for volume in volumes:
        volume_id = volume['VolumeId']
        
        # Create snapshot
        snapshot = ec2.create_snapshot(VolumeId=volume_id, Description='Backup for volume {}'.format(volume_id))
        print('Snapshot created for volume {}: {}'.format(volume_id, snapshot['SnapshotId']))
        
        # Get current date
        current_date = datetime.now()
        
        # Describe snapshots for volume
        snapshots = ec2.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])['Snapshots']
        
        # Tag snapshots with volume attachment information
        for snap in snapshots:
            ec2.create_tags(
                Resources=[snap['SnapshotId']],
                Tags=[
                    {'Key': 'VolumeId', 'Value': volume_id},
                    {'Key': 'InstanceId', 'Value': volume['Attachments'][0]['InstanceId']},
                    {'Key': 'Device', 'Value': volume['Attachments'][0]['Device']}
                ]
            )
            print('Snapshot {} tagged with volume attachment information.'.format(snap['SnapshotId']))
        
        # Delete snapshots older than 15 days
        for snap in snapshots:
            snapshot_date = snap['StartTime'].replace(tzinfo=None)
            if (current_date - snapshot_date) > timedelta(days=15):
                ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
                print('Snapshot {} deleted as it is older than 15 days.'.format(snap['SnapshotId']))
