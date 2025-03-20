#!/usr/bin/env python3
import sys
import logging
from typing import Any
from src.main import initialize_jira

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_jira_connection() -> None:
    """Test the JIRA connection using the initialize_jira function."""
    try:
        # Initialize JIRA client using our package's function
        jira = initialize_jira()
        assert jira is not None, "JIRA client should not be None"
        
        # Test connection by fetching user information
        myself = jira.myself()
        logger.info(f"Successfully connected to JIRA as {myself['displayName']}")
        assert myself is not None, "User information should not be None"
        
        # Get some projects as a further test
        projects = jira.projects()
        logger.info(f"Found {len(projects)} projects:")
        
        for project in projects[:5]:  # Display first 5 projects
            logger.info(f"  - {project.name} ({project.key})")
        if len(projects) > 5:
            logger.info(f"  - ... and {len(projects) - 5} more")
        
        assert len(projects) > 0, "Should find at least one project"
    except Exception as e:
        logger.error(f"Error connecting to JIRA: {e}")
        raise AssertionError(f"JIRA connection failed: {e}")

# Remove the script execution block since we'll only use pytest to run this test