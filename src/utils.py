import re
import boto3


def convert_json_string(json_string):
    pass


def extract_file_from_bucket(bucket, key, s3_client=None):
    if not s3_client:
        s3_client = boto3.client("s3")

    response = s3_client.get_object(Bucket=bucket, Key=key)
