import boto3
from utils import get_s3_object, obfuscate_fields


def obfuscate_csv(event):
    """Main function to process CSV obfuscation."""
    s3_client = boto3.client("s3")
    csv_content, _, _ = get_s3_object(s3_client, event["file_to_obfuscate"])
    return obfuscate_fields(csv_content, event["pii_fields"])
