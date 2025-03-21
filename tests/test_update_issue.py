#!/usr/bin/env python3
"""Test the JIRA issue update tool with mocking."""
import unittest
from unittest.mock import patch, MagicMock
import logging
from src.tools.issues import update_issue

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestUpdateIssue(unittest.TestCase):
    """Test cases for update_issue using mocks."""
    
    @patch('src.tools.issues.initialize_jira')
    def test_update_issue(self, mock_initialize_jira):
        """Test the update_issue function with mocked JIRA client."""
        # Create a mock JIRA client
        mock_jira = MagicMock()
        mock_initialize_jira.return_value = mock_jira
        
        # Set up the mock issue
        mock_issue = MagicMock()
        mock_issue.key = "TEST-123"
        
        # Set up issue fields
        mock_fields = MagicMock()
        mock_fields.summary = "Updated Summary"
        mock_fields.status = MagicMock()
        mock_fields.status.name = "In Progress"
        mock_issue.fields = mock_fields
        
        # Mock jira.issue() method to return our mock_issue
        mock_jira.issue.return_value = mock_issue
        
        # Mock transitions
        mock_transition = {'id': 'transition-id', 'name': 'In Progress'}
        mock_jira.transitions.return_value = [mock_transition]
        
        # Set server option for URL generation
        mock_jira._options = {'server': 'https://jira.example.com'}
        
        # Test data
        issue_key = "TEST-123"
        summary = "Updated Summary"
        description = "Updated Description"
        status = "In Progress"
        priority = "High"
        assignee = "johndoe"
        comment = "This is a test comment"
        
        # Call the function
        result = update_issue(
            issue_key=issue_key,
            summary=summary,
            description=description,
            status=status,
            priority=priority,
            assignee=assignee,
            comment=comment
        )
        
        # Verify mock was called with correct parameters
        mock_initialize_jira.assert_called_once()
        mock_jira.issue.assert_called()
        
        # Verify update calls
        mock_issue.update.assert_any_call(fields={'summary': summary})
        mock_issue.update.assert_any_call(fields={'description': description})
        mock_issue.update.assert_any_call(fields={'priority': {'name': priority}})
        mock_issue.update.assert_any_call(fields={'assignee': {'name': assignee}})
        
        # Verify comment was added
        mock_jira.add_comment.assert_called_once_with(mock_issue, comment)
        
        # Verify transition was called
        mock_jira.transitions.assert_called_once_with(mock_issue)
        mock_jira.transition_issue.assert_called_once_with(mock_issue, 'transition-id')
        
        # Verify the result format
        self.assertEqual(result['key'], "TEST-123")
        self.assertEqual(result['summary'], "Updated Summary")
        self.assertEqual(result['status'], "In Progress")
        self.assertTrue(isinstance(result['changes'], list))
        self.assertEqual(result['url'], "https://jira.example.com/browse/TEST-123")
        
        # Verify all expected changes are in the response
        changes = result['changes']
        self.assertIn(f"Summary updated to: {summary}", changes)
        self.assertIn("Description updated", changes)
        self.assertIn(f"Priority set to: {priority}", changes)
        self.assertIn(f"Assigned to: {assignee}", changes)
        self.assertIn("Comment added", changes)
        self.assertIn(f"Status changed to: {status}", changes)
        
        logger.info(f"Simulated update of issue: {result['key']} - {result['summary']}")
        logger.info(f"Changes: {', '.join(result['changes'])}")


if __name__ == '__main__':
    unittest.main()