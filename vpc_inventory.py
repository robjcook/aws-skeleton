import boto3
import csv

# Initialize a boto3 session
session = boto3.Session()

# Clients for different AWS services
ec2_client = session.client('ec2')
rds_client = session.client('rds')
elbv2_client = session.client('elbv2')
elasticache_client = session.client('elasticache')
redshift_client = session.client('redshift')
efs_client = session.client('efs')

# Specify the VPC ID you want to gather resources for
vpc_id = 'your-vpc-id'

# Function to write resources to CSV
def write_to_csv(data, filename="vpc_resources.csv"):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data written to {filename}")

# Function to collect and log VPC-associated resources
def collect_vpc_resources(vpc_id):
    resources = []

    # Get Subnets
    subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for subnet in subnets['Subnets']:
        resources.append({
            'ResourceType': 'Subnet',
            'ResourceId': subnet['SubnetId'],
            'CIDR': subnet['CidrBlock'],
            'State': subnet['State']
        })

    # Get Route Tables
    route_tables = ec2_client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for rt in route_tables['RouteTables']:
        resources.append({
            'ResourceType': 'RouteTable',
            'ResourceId': rt['RouteTableId'],
            'Routes': str([route['DestinationCidrBlock'] for route in rt['Routes'] if 'DestinationCidrBlock' in route])
        })

    # Get Security Groups
    security_groups = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for sg in security_groups['SecurityGroups']:
        resources.append({
            'ResourceType': 'SecurityGroup',
            'ResourceId': sg['GroupId'],
            'GroupName': sg['GroupName'],
            'Description': sg['Description']
        })

    # Get Internet Gateways
    igws = ec2_client.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}])
    for igw in igws['InternetGateways']:
        resources.append({
            'ResourceType': 'InternetGateway',
            'ResourceId': igw['InternetGatewayId']
        })

    # Get NAT Gateways
    nat_gateways = ec2_client.describe_nat_gateways(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for nat in nat_gateways['NatGateways']:
        resources.append({
            'ResourceType': 'NATGateway',
            'ResourceId': nat['NatGatewayId'],
            'State': nat['State']
        })

    # Get Elastic IPs
    eips = ec2_client.describe_addresses(Filters=[{'Name': 'domain', 'Values': ['vpc']}])
    for eip in eips['Addresses']:
        if 'NetworkInterfaceId' in eip:
            resources.append({
                'ResourceType': 'ElasticIP',
                'ResourceId': eip['PublicIp'],
                'AllocationId': eip['AllocationId']
            })

    # Get VPC Peering Connections
    vpc_peerings = ec2_client.describe_vpc_peering_connections(Filters=[{'Name': 'requester-vpc-info.vpc-id', 'Values': [vpc_id]}])
    for vpc_peering in vpc_peerings['VpcPeeringConnections']:
        resources.append({
            'ResourceType': 'VpcPeeringConnection',
            'ResourceId': vpc_peering['VpcPeeringConnectionId'],
            'Status': vpc_peering['Status']['Code']
        })

    # Get RDS instances
    rds_instances = rds_client.describe_db_instances()
    for db_instance in rds_instances['DBInstances']:
        if db_instance['DBSubnetGroup']['VpcId'] == vpc_id:
            resources.append({
                'ResourceType': 'RDSInstance',
                'ResourceId': db_instance['DBInstanceIdentifier'],
                'DBInstanceClass': db_instance['DBInstanceClass']
            })

    # Get Load Balancers (ALB/NLB)
    load_balancers = elbv2_client.describe_load_balancers()
    for lb in load_balancers['LoadBalancers']:
        if lb['VpcId'] == vpc_id:
            resources.append({
                'ResourceType': 'LoadBalancer',
                'ResourceId': lb['LoadBalancerArn'],
                'Type': lb['Type']
            })

    # Get ElastiCache clusters
    cache_clusters = elasticache_client.describe_cache_clusters()
    for cluster in cache_clusters['CacheClusters']:
        if 'CacheSubnetGroupName' in cluster and cluster['Engine'] == 'redis':
            resources.append({
                'ResourceType': 'ElastiCacheCluster',
                'ResourceId': cluster['CacheClusterId'],
                'Engine': cluster['Engine']
            })

    # Get Redshift clusters
    redshift_clusters = redshift_client.describe_clusters()
    for cluster in redshift_clusters['Clusters']:
        if cluster['VpcId'] == vpc_id:
            resources.append({
                'ResourceType': 'RedshiftCluster',
                'ResourceId': cluster['ClusterIdentifier'],
                'NodeType': cluster['NodeType']
            })

    # Get EFS File Systems
    efs_filesystems = efs_client.describe_file_systems()
    for fs in efs_filesystems['FileSystems']:
        for mount_target in efs_client.describe_mount_targets(FileSystemId=fs['FileSystemId'])['MountTargets']:
            if mount_target['VpcId'] == vpc_id:
                resources.append({
                    'ResourceType': 'EFSFileSystem',
                    'ResourceId': fs['FileSystemId'],
                    'MountTargetId': mount_target['MountTargetId']
                })

    return resources

# Collect resources for the specified VPC
vpc_resources = collect_vpc_resources(vpc_id)

# Write resources to CSV
if vpc_resources:
    write_to_csv(vpc_resources)
else:
    print("No resources found for the VPC.")
