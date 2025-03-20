#!/usr/bin/env python3
"""Test the JIRA issue creation tool with mocking."""
import unittest
from unittest.mock import patch, MagicMock
import logging
from src.tools.issues import create_issue

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestCreateIssue(unittest.TestCase):
    """Test cases for create_issue using mocks."""
    
    @patch('src.tools.issues.initialize_jira')
    def test_create_issue(self, mock_initialize_jira):
        """Test the create_issue function with mocked JIRA client."""
        # Create a mock JIRA client
        mock_jira = MagicMock()
        mock_initialize_jira.return_value = mock_jira
        
        # Set up the mock for create_issue return value
        mock_issue = MagicMock()
        mock_issue.key = "TEST-123"
        mock_jira.create_issue.return_value = mock_issue
        
        # Set server option for URL generation
        mock_jira._options = {'server': 'https://jira.example.com'}
        
        # Test data
        project_key = "TEST"
        summary = "Test Issue"
        description = "Test Description"
        
        # Call the function
        result = create_issue(
            project_key=project_key,
            summary=summary,
            description=description,
            issue_type="Bug",
            priority="High"
        )
        
        # Verify mock was called with correct parameters
        mock_initialize_jira.assert_called_once()
        mock_jira.create_issue.assert_called_once()
        
        # Get the call arguments
        args, kwargs = mock_jira.create_issue.call_args
        
        # Verify the fields in the issue creation request
        fields = kwargs.get('fields', {})
        self.assertEqual(fields['project']['key'], project_key)
        self.assertEqual(fields['summary'], summary)
        self.assertEqual(fields['description'], description)
        self.assertEqual(fields['issuetype']['name'], "Bug")
        self.assertEqual(fields['priority']['name'], "High")
        
        # Verify the result format
        self.assertEqual(result['key'], "TEST-123")
        self.assertEqual(result['summary'], summary)
        self.assertEqual(result['project'], project_key)
        self.assertEqual(result['url'], "https://jira.example.com/browse/TEST-123")
        
        logger.info(f"Simulated creation of issue: {result['key']} - {result['summary']}")
        logger.info(f"Issue would be at URL: {result['url']}")


if __name__ == '__main__':
    unittest.main()