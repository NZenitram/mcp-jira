#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from jira import JIRA

# Load environment variables from .env file
load_dotenv()

def initialize_jira():
    """Initialize and return JIRA client connection using environment variables."""
    jira_server = os.getenv("JIRA_SERVER")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    
    if not all([jira_server, jira_email, jira_api_token]):
        raise ValueError("Missing required JIRA environment variables")
    
    jira = JIRA(
        server=jira_server,
        basic_auth=(jira_email, jira_api_token)
    )
    return jira

def main():
    # Initialize JIRA connection
    jira_client = initialize_jira()
    
    # Initialize FastMCP
    app = FastMCP(name="jira-tools")
    
    # Import tools
    from src.tools.issues import search_issues, create_issue, update_issue, delete_issue, add_comment
    from src.tools.projects import list_projects
    
    # Register tools using the add_tool method  
    app.add_tool(
        list_projects,
        name="list_projects",
        description="List JIRA projects for the authenticated user"
    )

    app.add_tool(
        search_issues,
        name="search_issues",
        description="Search for JIRA issues using JQL (JIRA Query Language)"
    )
  
    app.add_tool(
        create_issue,
        name="create_issue",
        description="Create a new JIRA issue in a specified project"
    )
    
    app.add_tool(
        update_issue,
        name="update_issue",
        description="Update an existing JIRA issue with new values"
    )
    
    app.add_tool(
        delete_issue,
        name="delete_issue",
        description="Delete a JIRA issue (requires explicit confirmation)"
    )

    app.add_tool(
        add_comment,
        name="add_comment",
        description="Add a comment to an existing JIRA issue"
    )
    
    # Start the FastMCP application
    app.run()

if __name__ == "__main__":
    main()