"""Server module for Jira.

This module re-exports the create_jira_server function from the jira_server module
to avoid circular imports while maintaining the API.
"""

from .jira_server import create_jira_server

__all__ = ["create_jira_server"] 