"""Service module for Jira API interactions."""

import logging
import os
from .config import JiraConfig
from .client import JiraClient
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

# Configure logging
logger = logging.getLogger(__name__)

class JiraService(
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
    """Jira service for API interactions."""

    def __init__(self, access_token: str = None, config: JiraConfig = None, cloud_id: str = None):
        """Initialize the Jira service with access token or config.

        Args:
            access_token: OAuth Bearer access token for Jira Cloud API
            config: Optional JiraConfig if not using access_token
            cloud_id: Optional Jira Cloud ID for cloud API endpoints
        """
        if access_token and not config:
            # Use cloud_id directly from parameter if provided, don't rely on environment variable
            if cloud_id:
                jira_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"
                auth_type = "oauth"
            else:
                logger.warning("No JIRA_URL or cloud_id provided")
                return
            
            # Create config with the token
            config = JiraConfig(
                url=jira_url,
                auth_type=auth_type,
                personal_token=access_token,
                ssl_verify=True
            )
            
        # Initialize the JiraClient with the config
        super().__init__(config=config) 