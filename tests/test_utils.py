import pytest
import io
import csv
from unittest.mock import MagicMock
from utils import get_s3_object, obfuscate_fields
from main import obfuscate_csv


def test_get_s3_object():
    mock_s3_client = MagicMock()
    mock_s3_client.get_object.return_value = {
        "Body": io.BytesIO(b"student_id,name,email\n1234,John Doe,john@email.com\n")
    }

    content, bucket, key = get_s3_object(mock_s3_client, "s3://test-bucket/test.csv")

    assert content == "student_id,name,email\n1234,John Doe,john@email.com\n"
    assert bucket == "test-bucket"
    assert key == "test.csv"


def test_obfuscate_fields():
    csv_content = "student_id,name,email\n1234,John Doe,john@email.com\n"
    pii_fields = ["name", "email"]

    obfuscated_output = obfuscate_fields(csv_content, pii_fields)
    obfuscated_output.seek(0)

    reader = csv.reader(io.StringIO(obfuscated_output.read().decode("utf-8")))
    rows = list(reader)

    assert rows[0] == ["student_id", "name", "email"]
    assert rows[1] == ["1234", "***", "***"]


def test_obfuscate_csv(mocker):
    mock_s3_client = MagicMock()
    mock_s3_client.get_object.return_value = {
        "Body": io.BytesIO(b"student_id,name,email\n1234,John Doe,john@email.com\n")
    }
    mocker.patch("main.boto3.client", return_value=mock_s3_client)

    event = {
        "file_to_obfuscate": "s3://test-bucket/test.csv",
        "pii_fields": ["name", "email"],
    }

    obfuscated_output = obfuscate_csv(event)
    obfuscated_output.seek(0)

    reader = csv.reader(io.StringIO(obfuscated_output.read().decode("utf-8")))
    rows = list(reader)

    assert rows[0] == ["student_id", "name", "email"]
    assert rows[1] == ["1234", "***", "***"]
