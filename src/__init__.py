# src/__init__.py
from .main import obfuscate_file  # Makes `obfuscate_file` accessible when importing src

__all__ = ["obfuscate_file"]  # Defines what gets imported with `from src import *`
