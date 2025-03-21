"""Tools for interacting with JIRA issues."""
from typing import List, Dict, Any, Optional, Union
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

def update_issue(
    issue_key: str,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing JIRA issue.
    
    Args:
        issue_key: The JIRA issue key (e.g., "PROJ-123")
        summary: New summary for the issue
        description: New description for the issue
        status: New status for the issue (transition)
        priority: New priority for the issue
        assignee: New assignee for the issue
        comment: Comment to add to the issue
        
    Returns:
        Dictionary containing the updated issue information
    """
    # Initialize JIRA client
    jira = initialize_jira()
    
    # Get the issue
    issue = jira.issue(issue_key)
    
    # Check if issue exists
    if not issue:
        raise ValueError(f"Issue {issue_key} not found")
    
    # Dictionary to track changes
    changes = []
    
    # Update fields
    if summary:
        issue.update(fields={'summary': summary})
        changes.append(f"Summary updated to: {summary}")
    
    if description:
        issue.update(fields={'description': description})
        changes.append("Description updated")
    
    if priority:
        issue.update(fields={'priority': {'name': priority}})
        changes.append(f"Priority set to: {priority}")
    
    if assignee:
        issue.update(fields={'assignee': {'name': assignee}})
        changes.append(f"Assigned to: {assignee}")
    
    # Add comment if provided
    if comment:
        jira.add_comment(issue, comment)
        changes.append("Comment added")
    
    # Handle status transition
    if status:
        # Get available transitions
        transitions = jira.transitions(issue)
        transition_id = None
        
        # Find the transition ID for the requested status
        for t in transitions:
            if t['name'].lower() == status.lower():
                transition_id = t['id']
                break
        
        # If transition is found, perform it
        if transition_id:
            jira.transition_issue(issue, transition_id)
            changes.append(f"Status changed to: {status}")
        else:
            available_statuses = [t['name'] for t in transitions]
            raise ValueError(f"Status '{status}' not found. Available statuses: {', '.join(available_statuses)}")
    
    # Refresh the issue data after updates
    updated_issue = jira.issue(issue_key)
    
    # Prepare response
    response = {
        'key': updated_issue.key,
        'summary': getattr(updated_issue.fields, 'summary', 'No summary'),
        'status': getattr(updated_issue.fields.status, 'name', 'Unknown') if hasattr(updated_issue.fields, 'status') else 'Unknown',
        'changes': changes,
        'url': f"{jira._options['server']}/browse/{updated_issue.key}"
    }
    
    return response

def delete_issue(
    issue_key: str,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Delete a JIRA issue.
    
    Args:
        issue_key: The JIRA issue key (e.g., "PROJ-123")
        confirm: Confirmation flag to prevent accidental deletion (must be True)
        
    Returns:
        Dictionary containing status of the deletion
    """
    # Require explicit confirmation
    if not confirm:
        raise ValueError("Deletion requires explicit confirmation. Set confirm=True to proceed.")
    
    # Initialize JIRA client
    jira = initialize_jira()
    
    # Get the issue to verify it exists and capture details for the response
    issue = jira.issue(issue_key)
    
    # Check if issue exists
    if not issue:
        raise ValueError(f"Issue {issue_key} not found")
    
    # Capture issue details before deletion
    summary = getattr(issue.fields, 'summary', 'No summary')
    project_key = issue_key.split('-')[0] if '-' in issue_key else 'Unknown'
    
    # Delete the issue
    issue.delete()
    
    # Prepare response
    return {
        'status': 'success',
        'message': f'Issue {issue_key} has been deleted',
        'details': {
            'key': issue_key,
            'summary': summary,
            'project': project_key
        }
    }

def add_comment(
    issue_key: str,
    comment: str
) -> Dict[str, Any]:
    """
    Add a comment to a JIRA issue.
    
    Args:
        issue_key: The JIRA issue key (e.g., "PROJ-123")
        comment: The comment text to add to the issue
        
    Returns:
        Dictionary containing the comment information and status
    """
    # Initialize JIRA client
    jira = initialize_jira()
    
    # Get the issue to verify it exists
    issue = jira.issue(issue_key)
    
    # Check if issue exists
    if not issue:
        raise ValueError(f"Issue {issue_key} not found")
    
    # Add the comment
    comment_obj = jira.add_comment(issue, comment)
    
    # Prepare response
    return {
        'status': 'success',
        'message': f'Comment added to issue {issue_key}',
        'details': {
            'issue_key': issue_key,
            'comment_id': comment_obj.id,
            'comment_text': comment,
            'author': getattr(comment_obj.author, 'displayName', 'Unknown'),
            'created': str(comment_obj.created),
            'url': f"{jira._options['server']}/browse/{issue_key}?focusedCommentId={comment_obj.id}"
        }
    }