import logging
from collections.abc import Sequence
from typing import Any
import traceback
import json

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
)

from .service import JiraService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-atlassian-jira")

def create_jira_server(jira_service: JiraService) -> Server:
    """
    Create an MCP server for Jira
    
    Args:
        jira_service: An initialized JiraService instance
        
    Returns:
        A configured MCP Server instance
    """
    server = Server("mcp-atlassian-jira")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="jira_get_issue",
                description="Get details of a specific Jira issue including its Epic links and relationship information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_key": {
                            "type": "string", 
                            "description": "Jira issue key (e.g., 'PROJ-123')",
                        },
                        "fields": {
                            "type": "string",
                            "description": "Fields to return. Can be a comma-separated list, '*all' for all fields, or omitted for essential fields only",
                        },
                        "expand": {
                            "type": "string",
                            "description": "Optional fields to expand. Examples: 'renderedFields', 'transitions', 'changelog'",
                        },
                        "comment_limit": {
                            "type": "number",
                            "description": "Maximum number of comments to include (0 or null for no comments)",
                        },
                    },
                    "required": ["issue_key"],
                },
            ),
            Tool(
                name="jira_search",
                description="Search Jira issues using JQL (Jira Query Language)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "jql": {
                            "type": "string",
                            "description": "JQL query string (Jira Query Language)",
                        },
                        "fields": {
                            "type": "string",
                            "description": "Comma-separated fields to return in the results",
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of results (1-50)",
                        },
                        "startAt": {
                            "type": "number",
                            "description": "Starting index for pagination (0-based)",
                        },
                    },
                    "required": ["jql"],
                },
            ),
        ]
    
    @server.call_tool()
    async def call_tool(
        name: str, arguments: Any
    ) -> Sequence[TextContent]:
        try:
            if not isinstance(arguments, dict):
                raise RuntimeError("arguments must be dictionary")
                
            if name == "jira_get_issue":
                issue_key = arguments.get("issue_key")
                fields = arguments.get("fields", "summary,description,status,assignee,reporter,labels,priority,created,updated,issuetype")
                expand = arguments.get("expand")
                comment_limit = arguments.get("comment_limit", 10)
                
                logger.debug(f"Fetching issue: {issue_key}")
                issue = jira_service.get_issue(
                    issue_key,
                    fields=fields,
                    expand=expand,
                    comment_limit=comment_limit
                )
                
                result = issue.to_simplified_dict() if hasattr(issue, "to_simplified_dict") else issue
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
                
            elif name == "jira_search":
                jql = arguments.get("jql")
                fields = arguments.get("fields", "summary,description,status,assignee,reporter,labels,priority,created,updated,issuetype")
                limit = min(int(arguments.get("limit", 10)), 50)
                start_at = int(arguments.get("startAt", 0))
                
                logger.debug(f"Searching with JQL: {jql}")
                search_result = jira_service.search_issues(
                    jql,
                    fields=fields,
                    limit=limit,
                    start=start_at
                )
                
                # Format results
                if hasattr(search_result, "issues"):
                    issues = [issue.to_simplified_dict() if hasattr(issue, "to_simplified_dict") else issue 
                             for issue in search_result.issues]
                    
                    # Include metadata in the response
                    response = {
                        "total": getattr(search_result, "total", 0),
                        "start_at": getattr(search_result, "start_at", 0),
                        "max_results": getattr(search_result, "max_results", len(issues)),
                        "issues": issues,
                    }
                else:
                    # Fallback if search_result doesn't have expected structure
                    response = search_result
                
                return [TextContent(type="text", text=json.dumps(response, indent=2))]
                
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(f"Error during call_tool: {str(e)}")
            raise RuntimeError(f"Caught Exception. Error: {str(e)}")
            
    return server 