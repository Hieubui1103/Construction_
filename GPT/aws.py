import boto3
import os
from dotenv import load_dotenv
load_dotenv()

def get_s3_file_urls(bucket_name = os.getenv("BUCKET_NAME"), folder_prefix = os.getenv("S3_PREFIX"), expiration=3600):
    """
    Retrieves the URLs of all files in a specific folder in an S3 bucket.

    Args:
        bucket_name (str): Name of the S3 bucket.
        folder_prefix (str): Prefix (folder path) to list objects under.

    Returns:
        List of URLs of the files in the specified folder.
    """
    s3_client = boto3.client('s3')
    urls = []
    
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                # Generate pre-signed URLs (optional) or public URLs
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': key},
                    ExpiresIn=expiration
                    )# f"https://{bucket_name}.s3.amazonaws.com/{key}"
                urls.append(url)
        
        print(f"Retrieved {len(urls)} file URLs from s3://{bucket_name}/{folder_prefix}")
    except Exception as e:
        print(f"Failed to retrieve file URLs. Error: {e}")
    
    return urls

# file_urls = get_s3_file_urls()
# # print(file_urls[0])
# # print(len(file_urls))
# # Print the URLs
# for url in file_urls:
#     print(url)
