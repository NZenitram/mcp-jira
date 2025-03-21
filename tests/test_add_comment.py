#!/usr/bin/env python3
"""Test the JIRA comment addition tool with mocking."""
import unittest
from unittest.mock import MagicMock, patch
import logging
from src.tools.issues import add_comment

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestAddComment(unittest.TestCase):
    """Test cases for add_comment using mocks."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.issue_key = "TEST-123"
        self.comment_text = "This is a test comment"
        
        # Mock comment object attributes
        self.mock_comment = MagicMock()
        self.mock_comment.id = "12345"
        self.mock_comment.created = "2024-03-21T10:00:00.000+0000"
        self.mock_comment.author.displayName = "Test User"

        # Mock issue object
        self.mock_issue = MagicMock()
        
        # Mock JIRA client
        self.mock_jira = MagicMock()
        self.mock_jira._options = {'server': 'https://test-jira.atlassian.net'}
        self.mock_jira.issue.return_value = self.mock_issue
        self.mock_jira.add_comment.return_value = self.mock_comment

    @patch('src.tools.issues.initialize_jira')
    def test_add_comment_success(self, mock_init_jira):
        """Test successful comment addition to an issue."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira

        # Call the function
        result = add_comment(self.issue_key, self.comment_text)

        # Verify JIRA client calls
        mock_init_jira.assert_called_once()
        self.mock_jira.issue.assert_called_once_with(self.issue_key)
        self.mock_jira.add_comment.assert_called_once_with(self.mock_issue, self.comment_text)

        # Verify response structure
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], f'Comment added to issue {self.issue_key}')
        self.assertEqual(result['details']['issue_key'], self.issue_key)
        self.assertEqual(result['details']['comment_id'], "12345")
        self.assertEqual(result['details']['comment_text'], self.comment_text)
        self.assertEqual(result['details']['author'], "Test User")
        self.assertEqual(result['details']['created'], "2024-03-21T10:00:00.000+0000")
        self.assertEqual(
            result['details']['url'],
            f"https://test-jira.atlassian.net/browse/{self.issue_key}?focusedCommentId=12345"
        )
        
        logger.info(f"Successfully added comment to issue: {self.issue_key}")
        logger.info(f"Comment ID: {result['details']['comment_id']}")

    @patch('src.tools.issues.initialize_jira')
    def test_add_comment_issue_not_found(self, mock_init_jira):
        """Test adding comment to non-existent issue."""
        # Set up mock to return None for non-existent issue
        self.mock_jira.issue.return_value = None
        mock_init_jira.return_value = self.mock_jira

        # Verify that attempting to add comment to non-existent issue raises ValueError
        with self.assertRaises(ValueError) as context:
            add_comment(self.issue_key, self.comment_text)

        self.assertEqual(str(context.exception), f"Issue {self.issue_key} not found")
        
        logger.info("Successfully prevented comment addition to non-existent issue")


if __name__ == '__main__':
    unittest.main() 