#!/usr/bin/env python3
"""Test the JIRA issue deletion tool with mocking."""
import unittest
from unittest.mock import patch, MagicMock
import logging
from src.tools.issues import delete_issue

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestDeleteIssue(unittest.TestCase):
    """Test cases for delete_issue using mocks."""
    
    @patch('src.tools.issues.initialize_jira')
    def test_delete_issue(self, mock_initialize_jira):
        """Test the delete_issue function with mocked JIRA client."""
        # Create a mock JIRA client
        mock_jira = MagicMock()
        mock_initialize_jira.return_value = mock_jira
        
        # Set up the mock issue
        mock_issue = MagicMock()
        mock_issue.key = "TEST-123"
        
        # Set up issue fields
        mock_fields = MagicMock()
        mock_fields.summary = "Test Issue to Delete"
        mock_issue.fields = mock_fields
        
        # Mock jira.issue() method to return our mock_issue
        mock_jira.issue.return_value = mock_issue
        
        # Test data
        issue_key = "TEST-123"
        
        # Call the function with confirm=True
        result = delete_issue(
            issue_key=issue_key,
            confirm=True
        )
        
        # Verify mock was called with correct parameters
        mock_initialize_jira.assert_called_once()
        mock_jira.issue.assert_called_once_with(issue_key)
        mock_jira.delete_issue.assert_called_once_with(issue_key)
        
        # Verify the result format
        self.assertEqual(result['key'], issue_key)
        self.assertEqual(result['summary'], "Test Issue to Delete")
        self.assertEqual(result['project'], "TEST")
        self.assertEqual(result['status'], "Deleted")
        self.assertIn("successfully deleted", result['message'])
        
        logger.info(f"Simulated deletion of issue: {result['key']} - {result['summary']}")
        logger.info(f"Result message: {result['message']}")
    
    @patch('src.tools.issues.initialize_jira')
    def test_delete_issue_without_confirmation(self, mock_initialize_jira):
        """Test the delete_issue function without confirmation."""
        # Test data
        issue_key = "TEST-123"
        
        # Call the function without confirm=True
        with self.assertRaises(ValueError) as context:
            delete_issue(issue_key=issue_key)
        
        # Verify error message
        self.assertIn("requires explicit confirmation", str(context.exception))
        
        # Verify delete was not called
        mock_initialize_jira.assert_not_called()
        
        logger.info("Successfully prevented deletion without confirmation")


if __name__ == '__main__':
    unittest.main()