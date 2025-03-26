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
make requirements
```

## Usage

### As a CLI Tool
You can use this tool via a command-line interface:

```sh
python src/main.py --s3-uri s3://my-bucket/my-file.csv --pii-fields name,email
```

**Arguments:**
- `--s3-uri` – S3 location of the file to be obfuscated
- `--pii-fields` – Comma-separated list of PII fields to obfuscate

### As an Imported Function
You can also import and use it within a Python script:

```python
from src.main import obfuscate_file

event = {
    "file_to_obfuscate": "s3://my-bucket/my-file.csv",
    "pii_fields": ["name", "email"]
}

obfuscated_file = obfuscate_file(event)
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
│   ├── main.py  # Contains `obfuscate_file` function
│   ├── utils/   # Contains helper functions (e.g., S3 operations, parsing, obfuscation)
│── tests/       # Unit tests
│── requirements.in  # Dependency definitions
│── requirements.txt # Compiled dependencies
│── Makefile     # Automation commands
│── README.md    # Documentation
```

## Contributing
1. Fork the repository and create a feature branch.
2. Ensure code quality with `make run-checks` and `make unit-test`.
3. Submit a pull request with a clear description.

## License
This project is licensed under the MIT License.
