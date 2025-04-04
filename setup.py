from setuptools import setup, find_packages

setup(
    name="gdpr-obfuscator",
    version="0.1.0",
    packages=find_packages(where="src"),  # Finds all packages inside 'src'
    package_dir={"": "src"},  # Sets 'src' as the root package directory
    install_requires=[
        "boto3",
        "pandas",
        "pyarrow"  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "gdpr-obfuscate=main:cli_entry_point"  # Enables CLI usage
        ]
    },
    python_requires=">=3.7",  # Ensures Python version compatibility
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)