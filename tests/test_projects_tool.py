#!/usr/bin/env python3
"""Test the JIRA projects tool."""
import logging
from typing import List, Dict, Any
from src.tools.projects import list_projects

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_list_projects() -> None:
    """Test the list_projects tool function."""
    try:
        # Call the function with a small limit
        projects = list_projects(limit=3)
        
        # Log the results
        logger.info(f"Found {len(projects)} projects:")
        for project in projects:
            logger.info(f"  - {project['name']} ({project['key']}) Lead: {project['lead']}")
        
        # Assertions
        assert isinstance(projects, list), "Result should be a list"
        assert len(projects) <= 3, "Should respect the limit parameter"
        
        if len(projects) > 0:
            # Check structure of project data
            project = projects[0]
            assert 'key' in project, "Project should have a key"
            assert 'name' in project, "Project should have a name"
            assert 'lead' in project, "Project should have lead information"
    
    except Exception as e:
        logger.error(f"Error testing list_projects: {e}")
        raise