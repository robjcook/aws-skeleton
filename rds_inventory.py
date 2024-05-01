import boto3
import pandas as pd

def get_rds_instances():
    
    # Create an RDS client
    rds_client = session.client('rds')
    
    # Get all RDS instances
    response = rds_client.describe_db_instances()
    
    # Extract instance details
    instances = response['DBInstances']
    
    # Create a list to store instance details
    instance_data = []
    
    # Append instance details to the list
    for instance in instances:
        instance_data.append({
            "Instance Identifier": instance['DBInstanceIdentifier'],
            "Engine": instance['Engine'],
            "Status": instance['DBInstanceStatus'],
            "Endpoint": instance['Endpoint']['Address']
        })
    
    # Create a DataFrame from the list
    df = pd.DataFrame(instance_data)
    
    # Write DataFrame to Excel file
    df.to_excel("rds_instances.xlsx", index=False)

if __name__ == "__main__":
    get_rds_instances()
