"""Jira API module for mcp_atlassian.

This module provides various Jira API client implementations.
"""

# flake8: noqa

# Base client class
from atlassian.jira import Jira
from .client import JiraClient
from .config import JiraConfig

# Service classes and functions
from .service import JiraService

# Mixin classes - these are used for composition in Jira operation classes
from .comments import CommentsMixin
from .epics import EpicsMixin
from .fields import FieldsMixin
from .formatting import FormattingMixin
from .issues import IssuesMixin
from .links import LinksMixin
from .projects import ProjectsMixin
from .search import SearchMixin
from .sprints import SprintsMixin
from .transitions import TransitionsMixin
from .users import UsersMixin
from .worklog import WorklogMixin
from .boards import BoardsMixin
from .attachments import AttachmentsMixin

# Define a Fetcher class that composes all mixins
class JiraFetcher(
    ProjectsMixin,
    FieldsMixin,
    FormattingMixin,
    TransitionsMixin,
    WorklogMixin,
    EpicsMixin,
    CommentsMixin,
    SearchMixin,
    IssuesMixin,
    UsersMixin,
    BoardsMixin,
    SprintsMixin,
    AttachmentsMixin,
    LinksMixin,
    JiraClient
):
    """
    The main Jira client class providing access to all Jira operations.
    This composes all mixins to create a full-featured client.
    """
    pass

# Import the server module last to avoid circular imports
# This is just for exports, JiraFetcher is already available in this module
from .server import create_jira_server

__all__ = [
    "JiraFetcher", 
    "JiraClient", 
    "JiraConfig", 
    "JiraService", 
    "create_jira_server",
    "Jira"
]
