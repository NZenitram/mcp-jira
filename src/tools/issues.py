"""Tools for interacting with JIRA issues."""
from typing import List, Dict, Any, Optional
from fastmcp.tools import Tool

from src.main import initialize_jira

def search_issues(
    jql: str,
    max_results: Optional[int] = 10,
    fields: Optional[str] = "summary,status,assignee,priority,issuetype"
) -> Dict[str, Any]:
    """
    Searches for JIRA issues using JQL (JIRA Query Language).

    Args:
        jql: JIRA Query Language string (e.g. "project=DEMO AND status=Open")
        max_results: Maximum number of results to return (default: 10)
        fields: Comma-separated list of fields to include in the results
    
    Returns:
        Dictionary containing total issues count and list of matching issues
    """
    # Initialize JIRA client
    jira = initialize_jira()
    
    # Parse fields
    field_list = [f.strip() for f in fields.split(",")]
    
    # Execute the search
    search_results = jira.search_issues(
        jql_str=jql,
        maxResults=max_results,
        fields=field_list
    )
    
    # Format response
    formatted_issues = []
    for issue in search_results:
        issue_data = {
            "key": issue.key,
            "summary": getattr(issue.fields, "summary", "No summary provided")
        }
        
        # Add status if available
        if hasattr(issue.fields, "status") and issue.fields.status:
            issue_data["status"] = issue.fields.status.name
        
        # Add assignee if available
        if hasattr(issue.fields, "assignee") and issue.fields.assignee:
            issue_data["assignee"] = issue.fields.assignee.displayName
        
        # Add priority if available
        if hasattr(issue.fields, "priority") and issue.fields.priority:
            issue_data["priority"] = issue.fields.priority.name
        
        # Add issue type if available
        if hasattr(issue.fields, "issuetype") and issue.fields.issuetype:
            issue_data["issuetype"] = issue.fields.issuetype.name
        
        formatted_issues.append(issue_data)
    
    return {
        "total": len(search_results),
        "issues": formatted_issues
    }

def create_issue(
    project_key: str,
    summary: str,
    description: Optional[str] = None,
    issue_type: Optional[str] = "Task",
    priority: Optional[str] = None,
    assignee: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new JIRA issue.
    
    Args:
        project_key: The key of the project to create the issue in
        summary: Issue summary
        description: Issue description
        issue_type: Type of issue (default: "Task")
        priority: Priority of the issue
        assignee: Username to assign the issue to
        
    Returns:
        Dictionary containing the created issue key and URL
    """
    # Initialize JIRA client
    jira = initialize_jira()
    
    # Prepare issue fields
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'issuetype': {'name': issue_type}
    }
    
    # Add optional fields if provided
    if description:
        issue_dict['description'] = description
    
    if priority:
        issue_dict['priority'] = {'name': priority}
    
    if assignee:
        issue_dict['assignee'] = {'name': assignee}
    
    # Create the issue
    new_issue = jira.create_issue(fields=issue_dict)
    
    # Prepare response
    response = {
        'key': new_issue.key,
        'summary': summary,
        'project': project_key,
        'url': f"{jira._options['server']}/browse/{new_issue.key}"
    }
    
    return response