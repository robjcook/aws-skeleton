import boto3

# S3 bucket and top-level folder
bucket_name = "my-bucket"
prefix = "my-folder/"  # Top-level folder

s3 = boto3.client('s3')

# Paginated listing to handle large numbers of objects
def list_objects_recursive(bucket, prefix):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            yield obj['Key']

# Fetch ACL for each object
def get_acls_for_objects(bucket, prefix):
    for key in list_objects_recursive(bucket, prefix):
        print(f"Getting ACL for: {key}")
        acl = s3.get_object_acl(Bucket=bucket, Key=key)
        print(acl)

# Run the function
get_acls_for_objects(bucket_name, prefix)