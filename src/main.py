import argparse
import boto3
from src.utils import (
    extract_s3_info,
    get_s3_object,
    detect_file_type,
    parse_file_content,
    obfuscate_csv,
    obfuscate_json,
    obfuscate_parquet,
    obfuscate_fields,
)


def obfuscate_file(event):
    """Main function to process file obfuscation."""
    s3_client = boto3.client("s3")
    bucket_name, file_key = extract_s3_info(event["file_to_obfuscate"])
    file_content = get_s3_object(s3_client, bucket_name, file_key)
    file_type = detect_file_type(file_key)
    parsed_data = parse_file_content(file_content, file_type)
    return obfuscate_fields(parsed_data, event["pii_fields"], file_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obfuscate PII fields in an S3 file")
    parser.add_argument(
        "--s3-uri", required=True, help="S3 URI of the file to obfuscate"
    )
    parser.add_argument(
        "--pii-fields", required=True, help="Comma-separated list of PII fields"
    )

    args = parser.parse_args()

    event = {"file_to_obfuscate": args.s3_uri, "pii_fields": args.pii_fields.split(",")}

    result = obfuscate_file(event)
