#!/usr/bin/env python3
"""Test the JIRA issues search tool."""
import logging
from typing import Dict, Any
from src.tools.issues import search_issues

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_search_issues() -> None:
    """Test the search_issues tool function."""
    try:
        # Use a generic JQL that should work on most JIRA instances
        result = search_issues(
            jql="created >= -30d",  # Issues created in the last 30 days
            max_results=5
        )
        
        # Log the results
        logger.info(f"Found {result['total']} issues:")
        for issue in result['issues']:
            summary = issue.get('summary', 'No summary')
            key = issue.get('key', 'No key')
            status = issue.get('status', 'Unknown status')
            logger.info(f"  - {key}: {summary} ({status})")
        
        # Assertions
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'total' in result, "Result should contain a total count"
        assert 'issues' in result, "Result should contain an issues list"
        assert isinstance(result['issues'], list), "Issues should be a list"
        
        if len(result['issues']) > 0:
            # Check structure of issue data
            issue = result['issues'][0]
            assert 'key' in issue, "Issue should have a key"
            assert 'summary' in issue, "Issue should have a summary"
    
    except Exception as e:
        logger.error(f"Error testing search_issues: {e}")
        raise