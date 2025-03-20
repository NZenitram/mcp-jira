"""Tools for interacting with JIRA projects."""
from typing import List, Dict, Any, Optional
from fastmcp.tools import Tool

from src.main import initialize_jira

def list_projects(
    limit: Optional[int] = 10
) -> List[Dict[str, Any]]:
    """
    Lists JIRA projects for the authenticated user.

    Args:
        limit: Maximum number of projects to return (default: 10)
    
    Returns:
        List of projects with their key, name, and lead information
    """
    # Initialize JIRA client
    jira = initialize_jira()
    
    # Get projects
    projects = jira.projects()
    
    # Limit results
    projects = projects[:limit]
    
    # Format response
    formatted_projects = []
    for project in projects:
        formatted_projects.append({
            "key": project.key,
            "name": project.name,
            "lead": getattr(project, "lead", {}).get("displayName", "Unknown") if hasattr(project, "lead") else "Unknown"
        })
    
    return formatted_projects