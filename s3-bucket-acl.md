To handle folders within folders (nested structures in S3), the process remains essentially the same, but you’ll need to ensure the logic accounts for all objects, regardless of how deeply they’re nested.

Amazon S3 doesn’t have real folders—everything is represented as a flat key structure with prefixes. For example:

my-folder/
my-folder/sub-folder1/file1.txt
my-folder/sub-folder1/file2.txt
my-folder/sub-folder2/file3.txt

To retrieve ACLs for all objects under my-folder/, including objects in subfolders, you need to:
	1.	Recursively list all objects under the top-level folder using the list-objects-v2 API with the --prefix option.
	2.	Iterate over all object keys, regardless of depth, to fetch their ACLs.

Using AWS CLI for Nested Folders

Here’s a Bash script to list all objects recursively and fetch their ACLs:

BUCKET_NAME="my-bucket"
FOLDER_NAME="my-folder/"

# Get the list of all object keys under the folder (recursively)
OBJECT_KEYS=$(aws s3api list-objects-v2 --bucket $BUCKET_NAME --prefix $FOLDER_NAME --query 'Contents[].Key' --output text)

# Loop through each object and fetch ACL
for OBJECT_KEY in $OBJECT_KEYS; do
  echo "Getting ACL for $OBJECT_KEY"
  aws s3api get-object-acl --bucket $BUCKET_NAME --key "$OBJECT_KEY"
done

This script works for all objects under my-folder/ and its subfolders because list-objects-v2 retrieves objects with the specified prefix, including nested ones.

Using Python (boto3) for Nested Folders

Here’s a Python script to handle nested folders and fetch ACLs:

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

Key Details

	1.	Recursive Listing: The list_objects_v2 API with a prefix automatically includes nested objects (e.g., my-folder/sub-folder1/file.txt).
	2.	Paginated Listing: For large datasets, the list_objects_v2 API uses pagination. This is handled by the paginator in boto3.
	3.	ACL Retrieval: The script or CLI command fetches ACLs for each individual object, regardless of its depth in the “folder” structure.

Example Output

For the folder structure:

my-folder/
my-folder/file1.txt
my-folder/sub-folder1/file2.txt
my-folder/sub-folder2/file3.txt

The script will output ACLs for:
	•	my-folder/file1.txt
	•	my-folder/sub-folder1/file2.txt
	•	my-folder/sub-folder2/file3.txt

Let me know if you’d like further assistance!