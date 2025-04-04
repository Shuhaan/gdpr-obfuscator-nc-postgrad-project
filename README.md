# GDPR Obfuscator

## Overview
This project provides a tool to obfuscate personally identifiable information (PII) in files stored in AWS S3. It supports CSV, JSON, and Parquet formats.

## Features
- Automatically detects file types (.csv, .json, .parquet)
- Obfuscates specified PII fields
- Fetches files from AWS S3
- Outputs obfuscated files as byte streams

## Installation
Ensure you have the required dependencies installed:

```sh
pip install .
```

For development mode:

```sh
pip install -e .
```

## Usage

### As a CLI Tool

Once installed, you can use this tool via the command line:

```sh
gdpr-obfuscate --s3-uri s3://my-bucket/my-file.csv --pii-fields name,email
```

Arguments:
-	--s3-uri – S3 location of the file to be obfuscated
-	--pii-fields – Comma-separated list of PII fields to obfuscate

### Where to View the Obfuscated Data

By default, the obfuscated data is printed to stdout. If the file is written back to S3, check the output location in the S3 bucket.

To save locally, redirect the output:

```sh
gdpr-obfuscate --s3-uri s3://my-bucket/my-file.csv --pii-fields name,email > obfuscated_output.csv
```

### As an Imported Function

You can also import and use it within a Python script:

```python
from gdpr_obfuscator.main import obfuscate_file

event = {
    "file_to_obfuscate": "s3://my-bucket/my-file.csv",
    "pii_fields": ["name", "email"]
}

obfuscated_file = obfuscate_file(event)
print(obfuscated_file)
```

## Developer Guide

### Setting Up the Environment
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/gdpr-obfuscator-nc-postgrad-project.git
   cd gdpr-obfuscator-nc-postgrad-project
   ```
2. Create a virtual environment and activate it:
   ```sh
   make create-environment
   ```
3. Install dependencies:
   ```sh
   make requirements
   ```

### Running Tests
Run the test suite with:

```sh
make unit-test
```

### Installing as a Library

To use this as a library module in other projects, install it via:

```sh
pip install .
```

Then import it in your scripts:

```sh
from gdpr_obfuscator.main import obfuscate_file
```

If running directly from the project without installation, set the PYTHONPATH:

```sh
export PYTHONPATH=$(pwd)/src
```

### Makefile Commands
The `Makefile` provides useful automation:

- **Create virtual environment:**
  ```sh
  make create-environment
  ```
- **Install dependencies:**
  ```sh
  make requirements
  ```
- **Set up development tools (bandit, safety, black, coverage):**
  ```sh
  make dev-setup
  ```
- **Run safety scan:**
  ```sh
  make safety-scan
  ```
- **Run bandit security check:**
  ```sh
  make run-bandit
  ```
- **Run black code formatting:**
  ```sh
  make run-black
  ```
- **Run unit tests:**
  ```sh
  make unit-test
  ```
- **Run coverage check:**
  ```sh
  make check-coverage
  ```
- **Run all checks (bandit, black, coverage):**
  ```sh
  make run-checks
  ```
- **Clean up environment:**
  ```sh
  make clean
  ```

## Project Structure
```
gdpr-obfuscator-nc-postgrad-project/
│── src/
│   ├── __init__.py  # Package initializer
│   ├── main.py      # Contains `obfuscate_file` function and CLI entry point
│   ├── utils/       # Contains helper functions (e.g., S3 operations, parsing, obfuscation)
│── tests/           # Unit tests
│── requirements.in  # Dependency definitions
│── requirements.txt # Compiled dependencies
│── setup.py         # Installation script
│── Makefile         # Automation commands
│── README.md        # Documentation
```

## Contributing
1. Fork the repository and create a feature branch.
2. Ensure code quality with `make run-checks` and `make unit-test`.
3. Submit a pull request with a clear description.

## License
This project is licensed under the MIT License.
