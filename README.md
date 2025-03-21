# JIRA MCP Tools

A Multi-Claude Program (MCP) for interacting with JIRA APIs through Claude Desktop.

## Features

- Search JIRA issues using JQL (JIRA Query Language)
- List JIRA projects for the authenticated user

## Setup

1. Install Claude Desktop
2. Add this MCP to Claude Desktop
3. Configure your JIRA credentials:
   - JIRA_SERVER: Your JIRA instance URL (e.g., https://your-domain.atlassian.net)
   - JIRA_EMAIL: Your JIRA email address
   - JIRA_API_TOKEN: Your JIRA API token

## Getting a JIRA API Token

1. Log in to your Atlassian account
2. Go to Account Settings > Security > Create and manage API tokens
3. Click "Create API token"
4. Give it a name (e.g., "Claude Desktop Integration")
5. Click "Create" and save the generated token securely

## Tools

### Search Issues

Search for JIRA issues using JQL (JIRA Query Language).

**Parameters:**
- jql: JIRA Query Language string (e.g., "project=DEMO AND status=Open")
- max_results: Maximum number of results to return (default: 10)
- fields: Comma-separated list of fields to include in the results (default: "summary,status,assignee,priority,issuetype")

### Create Issue

Create a new JIRA issue in a specified project.

**Parameters:**
- project_key: The key of the project to create the issue in (e.g., "DEMO")
- summary: Issue summary
- description: Issue description (optional)
- issue_type: Type of issue (default: "Task", can be "Bug", "Story", etc.)
- priority: Priority of the issue (optional, e.g., "High", "Medium", "Low")
- assignee: Username to assign the issue to (optional)

### Update Issue

Update an existing JIRA issue with new values.

**Parameters:**
- issue_key: The JIRA issue key (e.g., "PROJ-123")
- summary: New summary for the issue (optional)
- description: New description for the issue (optional)
- status: New status for the issue (optional, e.g., "In Progress", "Done")
- priority: New priority for the issue (optional, e.g., "High", "Medium", "Low")
- assignee: New assignee for the issue (optional)
- comment: Comment to add to the issue (optional)

### Delete Issue

Delete a JIRA issue (requires explicit confirmation).

**Parameters:**
- issue_key: The JIRA issue key (e.g., "PROJ-123")
- confirm: Confirmation flag to prevent accidental deletion, must be set to True

### List Projects

Lists JIRA projects for the authenticated user.

**Parameters:**
- limit: Maximum number of projects to return (default: 10)

### Add Comment

Add a comment to an existing JIRA issue.

**Parameters:**
- issue_key: The JIRA issue key (e.g., "PROJ-123")
- comment: The comment text to add to the issue

### Transition Issue

Transition a JIRA issue to a new status.

**Parameters:**
- issue_key: The JIRA issue key (e.g., "PROJ-123")
- status: The target status to transition the issue to (e.g., "In Progress", "Done")
- comment: Optional comment to add with the transition

### Get Issue Details

Get detailed information about a JIRA issue.

**Parameters:**
- issue_key: The JIRA issue key (e.g., "PROJ-123")
- include_comments: Whether to include issue comments in the response (default: False)

## Example Usage

```
Search for bugs in the PROJECT with high priority:
search_issues(jql="project=PROJECT AND issuetype=Bug AND priority=High")

Create a new bug in the PROJECT:
create_issue(project_key="PROJECT", summary="Login button not working", description="Users cannot log in using the login button on the homepage", issue_type="Bug", priority="High")

Update an existing issue:
update_issue(issue_key="PROJECT-123", summary="Updated: Login button fixed", status="In Progress", comment="Fixed the CSS styling issue")

Delete an issue:
delete_issue(issue_key="PROJECT-123", confirm=True)

List the first 5 projects:
list_projects(limit=5)

Add a comment to an issue:
add_comment(issue_key="PROJECT-123", comment="The fix has been deployed to production")

Transition an issue:
transition_issue(issue_key="PROJECT-123", status="In Progress", comment="Starting work on this issue")

Get issue details:
get_issue_details(issue_key="PROJECT-123", include_comments=True)
```

## Development

For developers who want to modify or extend this MCP:

1. Clone the repository
2. Set up a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `python -m pytest`
5. Make your changes
6. Test with Claude Desktop