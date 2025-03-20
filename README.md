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

### List Projects

Lists JIRA projects for the authenticated user.

**Parameters:**
- limit: Maximum number of projects to return (default: 10)

## Example Usage

```
Search for bugs in the PROJECT with high priority:
search_issues(jql="project=PROJECT AND issuetype=Bug AND priority=High")

Create a new bug in the PROJECT:
create_issue(project_key="PROJECT", summary="Login button not working", description="Users cannot log in using the login button on the homepage", issue_type="Bug", priority="High")

List the first 5 projects:
list_projects(limit=5)
```

## Development

For developers who want to modify or extend this MCP:

1. Clone the repository
2. Set up a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `python -m pytest`
5. Make your changes
6. Test with Claude Desktop