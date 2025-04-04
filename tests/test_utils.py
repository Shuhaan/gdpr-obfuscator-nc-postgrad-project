import pytest
import io
import json
import pandas as pd
from unittest.mock import MagicMock
from src.utils import (
    extract_s3_info,
    detect_file_type,
    parse_file_content,
    obfuscate_csv,
    obfuscate_json,
    obfuscate_parquet,
    obfuscate_fields,
    get_s3_object,
)
from src.main import obfuscate_file


def test_extract_s3_info():
    file_location = "s3://my_bucket/path/to/file.csv"
    bucket, key = extract_s3_info(file_location)
    assert bucket == "my_bucket"
    assert key == "path/to/file.csv"


def test_detect_file_type():
    assert detect_file_type("data.csv") == "csv"
    assert detect_file_type("data.json") == "json"
    assert detect_file_type("data.parquet") == "parquet"
    with pytest.raises(ValueError):
        detect_file_type("data.txt")


def test_parse_file_content():
    csv_data = b"name,email\nJohn Doe,john@email.com\n"
    json_data = b'{"name": "John Doe", "email": "john@email.com"}'
    parquet_df = pd.DataFrame({"name": ["John Doe"], "email": ["john@email.com"]})
    parquet_io = io.BytesIO()
    parquet_df.to_parquet(parquet_io, index=False)

    assert parse_file_content(csv_data, "csv") == csv_data.decode("utf-8")
    assert parse_file_content(json_data, "json") == json.loads(
        json_data.decode("utf-8")
    )
    assert parse_file_content(parquet_io.getvalue(), "parquet").equals(parquet_df)


def test_obfuscate_csv():
    csv_input = "name,email\nJohn Doe,john@email.com\n"
    pii_fields = ["name", "email"]
    obfuscated_output = obfuscate_csv(csv_input, pii_fields).getvalue().decode("utf-8")
    assert "***" in obfuscated_output
    assert "John Doe" not in obfuscated_output


def test_obfuscate_json():
    json_input = {"name": "John Doe", "email": "john@email.com"}
    pii_fields = ["name", "email"]
    obfuscated_output = (
        obfuscate_json(json_input, pii_fields).getvalue().decode("utf-8")
    )
    assert "***" in obfuscated_output
    assert "John Doe" not in obfuscated_output


def test_obfuscate_parquet():
    df = pd.DataFrame({"name": ["John Doe"], "email": ["john@email.com"]})
    pii_fields = ["name", "email"]
    obfuscated_output = obfuscate_parquet(df, pii_fields)
    df_obfuscated = pd.read_parquet(obfuscated_output)
    assert df_obfuscated["name"].iloc[0] == "***"
    assert df_obfuscated["email"].iloc[0] == "***"


def test_get_s3_object(mocker):
    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": io.BytesIO(b"test data")}
    result = get_s3_object(mock_s3, "my_bucket", "file.csv")
    assert result == b"test data"


def test_obfuscate_file(mocker):
    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {
        "Body": io.BytesIO(b"name,email\nJohn Doe,john@email.com\n")
    }
    mocker.patch("boto3.client", return_value=mock_s3)

    event = {
        "file_to_obfuscate": "s3://my_bucket/file.csv",
        "pii_fields": ["name", "email"],
    }
    obfuscated_output = obfuscate_file(event)
    obfuscated_output.seek(0)

    assert "***" in obfuscated_output.read().decode("utf-8")
