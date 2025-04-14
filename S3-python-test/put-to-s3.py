import boto3
from botocore.client import Config

# MinIO settings
minio_endpoint = "http://localhost:9000"
access_key = "test"
secret_key = "testtest"
bucket_name = "test"
object_name = "coucou.txt"
file_path = "./coucou.txt"

# Create the S3 client with MinIO settings
s3 = boto3.client(
    's3',
    endpoint_url=minio_endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version='s3v4'),
    region_name='fr-gre-0'  # Can be anything for MinIO
)

# Create the bucket (optional: only if it doesn't exist)
try:
    s3.head_bucket(Bucket=bucket_name)
except:
    s3.create_bucket(Bucket=bucket_name)

# Upload the file
s3.upload_file(file_path, bucket_name, object_name)

print(f"✅ File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")