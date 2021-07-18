"""Utilities module."""
import os


def is_local():
    """Determine if the project is running locally."""
    return os.environ.get("ENVIRONMENT") in [None, "local"]


def is_dev():
    """Determine if the project is running locally."""
    return os.environ.get("ENVIRONMENT") in ["dev", "development"]


def is_prod():
    """Determine if the project is running locally."""
    return os.environ.get("ENVIRONMENT") in ["prod", "production"]
