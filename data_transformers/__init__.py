# We only want to expose the final piepline to the project.
# This helps with modularity and encapsulation -> OOP

from .sanitize_pipeline import get_sanitized_data

__all__ = ["get_sanitized_data"]
