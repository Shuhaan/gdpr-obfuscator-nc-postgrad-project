import boto3
import io
import csv
import json
import pandas as pd


def extract_s3_info(file_location):
    """Extract bucket name and file key from S3 URI."""
    s3_parts = file_location.replace("s3://", "").split("/", 1)
    return s3_parts[0], s3_parts[1]


def get_s3_object(s3_client, bucket_name, file_key):
    """Retrieve file from S3 and return its content."""
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return response["Body"].read()


def detect_file_type(file_key):
    """Determine the file type based on the file extension."""
    if file_key.endswith(".csv"):
        return "csv"
    elif file_key.endswith(".json"):
        return "json"
    elif file_key.endswith(".parquet"):
        return "parquet"
    else:
        raise ValueError("Unsupported file format")


def parse_file_content(file_content, file_type):
    """Parse file content based on type."""
    if file_type == "csv":
        return file_content.decode("utf-8")
    elif file_type == "json":
        return json.loads(file_content.decode("utf-8"))
    elif file_type == "parquet":
        return pd.read_parquet(io.BytesIO(file_content))


def obfuscate_csv(data, pii_fields):
    """Obfuscate specified fields in CSV data."""
    pii_fields = set(pii_fields)
    input_stream = io.StringIO(data)
    reader = csv.DictReader(input_stream)
    output_stream = io.StringIO()
    writer = csv.DictWriter(output_stream, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        for field in pii_fields:
            if field in row:
                row[field] = "***"
        writer.writerow(row)

    return io.BytesIO(output_stream.getvalue().encode("utf-8"))


def obfuscate_json(data, pii_fields):
    """Recursively obfuscate specified fields in JSON data."""

    def obfuscate(obj):
        if isinstance(obj, dict):
            return {
                k: ("***" if k in pii_fields else obfuscate(v)) for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [obfuscate(item) for item in obj]
        else:
            return obj

    obfuscated_json = obfuscate(data)
    return io.BytesIO(json.dumps(obfuscated_json).encode("utf-8"))


def obfuscate_parquet(data, pii_fields):
    """Obfuscate specified fields in Parquet data."""
    df = data.copy()
    for field in pii_fields:
        if field in df.columns:
            df[field] = "***"
    output_stream = io.BytesIO()
    df.to_parquet(output_stream, index=False)
    output_stream.seek(0)
    return output_stream


def obfuscate_fields(data, pii_fields, file_type):
    """Apply obfuscation based on file type."""
    if file_type == "csv":
        return obfuscate_csv(data, pii_fields)
    elif file_type == "json":
        return obfuscate_json(data, pii_fields)
    elif file_type == "parquet":
        return obfuscate_parquet(data, pii_fields)
