# JIRA MCP Tools

A Multi-Claude Program (MCP) for interacting with JIRA APIs through Claude Desktop.

## Features

- Search JIRA issues using JQL (JIRA Query Language)
- List JIRA projects for the authenticated user
- Create, update, and delete JIRA issues
- Add comments and transition issues between statuses
- Search for users (with GDPR compliance support)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mcp-jira.git
   cd mcp-jira
   ```

2. Create and activate a virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

5. Add your JIRA credentials to the `.env` file:
   ```
   JIRA_SERVER=https://your-domain.atlassian.net
   JIRA_EMAIL=your.email@example.com
   JIRA_API_TOKEN=your_api_token_here
   ```

6. Test the installation:
   ```bash
   # Run all tests
   python -m pytest

   # Run a specific test file
   python -m pytest tests/test_search_issues.py
   ```

7. Start the MCP server:
   ```bash
   python run.py
   ```

## Environment Setup

### JIRA API Token
You'll need a JIRA API token to authenticate with your JIRA instance:

1. Log in to your Atlassian account
2. Go to Account Settings > Security > Create and manage API tokens
3. Click "Create API token"
4. Give it a name (e.g., "Claude Desktop Integration")
5. Click "Create" and save the generated token securely

### GDPR Compliance
If you're using a JIRA Cloud instance (which is likely in GDPR strict mode):

1. User searches will only match against display names and email addresses
2. Username-based searches are not supported
3. Results may be limited based on user permissions
4. The tool automatically handles GDPR requirements, but you may need to adjust your search patterns

### Troubleshooting

Common issues and solutions:

1. **ModuleNotFoundError: No module named 'src'**
   ```bash
   # Run with PYTHONPATH set
   PYTHONPATH=/path/to/mcp-jira python run.py
   ```

2. **JIRA API Authentication Error**
   - Verify your API token is correct
   - Check that your email matches your Atlassian account
   - Ensure your JIRA instance URL is correct and includes 'https://'

3. **GDPR-related Errors**
   - If you see "username parameter not supported" errors, your instance is in GDPR mode
   - Use display names or email addresses for searching instead of usernames
   - The tool will automatically adjust the API calls for GDPR compliance

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

### Search Users

Search for JIRA users by name, email, or username. This tool helps you find users when you need to assign issues or add watchers.

> **Important Note**: For JIRA Cloud instances with GDPR strict mode enabled (which is the default for newer instances), user search must use the `query` parameter instead of `username`. The tool automatically handles this, but you may need to adjust your search patterns accordingly.

Parameters:
- `query` (str): The search string to match against user display names and email addresses
  - For GDPR-compliant instances, this searches display names and email addresses
  - The search is case-insensitive and matches partial strings
  - Example: "john" will match "John Doe" and "johnny@example.com"
- `max_results` (int, optional): Maximum number of users to return (default: 10)
- `include_active_users` (bool, optional): Include active users in search results (default: True)
- `include_inactive_users` (bool, optional): Include inactive users in search results (default: False)

Example usage:
```python
# Search for users with "john" in their display name or email
search_users(query="john")

# Search for up to 20 users, including inactive ones
search_users(
    query="smith",
    max_results=20,
    include_inactive_users=True
)
```

GDPR Compliance Notes:
- In GDPR strict mode, user search is more restrictive to protect user privacy
- The search matches against user display names and email addresses only
- Exact username matching is not supported
- The search is always case-insensitive
- Partial matches are supported (e.g., "jo" will match "John")
- Results may be limited based on the user's permissions and privacy settings

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