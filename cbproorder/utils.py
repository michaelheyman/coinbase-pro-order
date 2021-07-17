"""Utilities module."""
import os


def is_local():
    """Determine if the project is running locally."""
    return os.environ.get("ENVIRONMENT", "development") in ["local", "development"]
