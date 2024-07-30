import boto3
import os

# Create an S3 client
s3 = boto3.client('s3')

# Define the bucket name and folder path
bucket_name = 'your-bucket-name'
folder_path = 'path/to/folder/'

# Get a list of files in the local folder
local_folder = '/path/to/local/folder'
files = os.listdir(local_folder)

# Upload each file with the content type "application/json"
for file in files:
    file_path = os.path.join(local_folder, file)
    # Set the content type
    content_type = 'application/json'
    # Upload the file to S3 with the specified content type
    s3.upload_file(file_path, bucket_name, folder_path + file, ExtraArgs={'ContentType': content_type})
