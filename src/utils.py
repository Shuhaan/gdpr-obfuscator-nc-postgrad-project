import boto3
import io
import csv
import json


def get_s3_object(s3_client, file_location):
    """Retrieve CSV file from S3 and return its content as a string."""
    s3_parts = file_location.replace("s3://", "").split("/", 1)
    bucket_name, file_key = s3_parts[0], s3_parts[1]
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return response["Body"].read().decode("utf-8"), bucket_name, file_key


def obfuscate_fields(csv_content, pii_fields):
    """Obfuscate specified fields in the CSV content."""
    pii_fields = set(pii_fields)
    input_stream = io.StringIO(csv_content)
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
