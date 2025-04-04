import boto3
import os

from dotenv import load_dotenv
load_dotenv()

def upload_folder_to_s3(folder_path, bucket_name, s3_prefix):
    """
    Uploads a folder and its contents to an S3 bucket.

    Args:
        folder_path (str): Path to the local folder.
        bucket_name (str): Name of the S3 bucket.
        s3_prefix (str): Optional S3 prefix (subfolder) to upload files under.
    """
    s3_client = boto3.client('s3')
    
    # Walk through the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Replace backslashes on Windows
            
            try:
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f"Uploaded: {local_path} to s3://{bucket_name}/{s3_path}")
            except Exception as e:
                print(f"Failed to upload {local_path} to s3://{bucket_name}/{s3_path}. Error: {e}")

# Replace with your folder path, S3 bucket name, and optional prefix
folder_path = r"C:\VScode\Construction_CV\train" 
bucket_name = os.getenv("BUCKET_NAME")
s3_prefix = os.getenv("S3_PREFIX")  # Leave empty "" for no prefix

upload_folder_to_s3(folder_path, bucket_name, s3_prefix)
