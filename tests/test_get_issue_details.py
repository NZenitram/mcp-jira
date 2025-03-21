#!/usr/bin/env python3
"""Test the JIRA issue details retrieval tool with mocking."""
import unittest
from unittest.mock import patch, MagicMock
import logging
from src.tools.issues import get_issue_details

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestGetIssueDetails(unittest.TestCase):
    """Test cases for get_issue_details using mocks."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.issue_key = "TEST-123"
        
        # Mock issue fields
        self.mock_fields = MagicMock()
        self.mock_fields.summary = "Test Issue"
        self.mock_fields.description = "Test Description"
        self.mock_fields.created = "2024-03-21T10:00:00.000+0000"
        self.mock_fields.updated = "2024-03-21T11:00:00.000+0000"
        self.mock_fields.labels = ["bug", "high-priority"]
        
        # Mock nested objects
        self.mock_fields.status = MagicMock()
        self.mock_fields.status.name = "In Progress"
        
        self.mock_fields.issuetype = MagicMock()
        self.mock_fields.issuetype.name = "Bug"
        
        self.mock_fields.project = MagicMock()
        self.mock_fields.project.key = "TEST"
        self.mock_fields.project.name = "Test Project"
        
        self.mock_fields.creator = MagicMock()
        self.mock_fields.creator.displayName = "John Creator"
        
        self.mock_fields.reporter = MagicMock()
        self.mock_fields.reporter.displayName = "Jane Reporter"
        
        self.mock_fields.assignee = MagicMock()
        self.mock_fields.assignee.displayName = "Bob Assignee"
        
        self.mock_fields.priority = MagicMock()
        self.mock_fields.priority.name = "High"
        
        # Mock comments
        mock_comment = MagicMock()
        mock_comment.id = "12345"
        mock_comment.body = "Test comment"
        mock_comment.author.displayName = "Comment Author"
        mock_comment.created = "2024-03-21T12:00:00.000+0000"
        mock_comment.updated = "2024-03-21T12:00:00.000+0000"
        
        self.mock_fields.comment = MagicMock()
        self.mock_fields.comment.comments = [mock_comment]
        
        # Mock issue object
        self.mock_issue = MagicMock()
        self.mock_issue.key = self.issue_key
        self.mock_issue.fields = self.mock_fields
        
        # Mock JIRA client
        self.mock_jira = MagicMock()
        self.mock_jira._options = {'server': 'https://test-jira.atlassian.net'}
        self.mock_jira.issue.return_value = self.mock_issue
        
        # Mock transitions
        self.mock_transitions = [
            {'id': '2', 'name': 'In Progress'},
            {'id': '3', 'name': 'Done'}
        ]
        self.mock_jira.transitions.return_value = self.mock_transitions

    @patch('src.tools.issues.initialize_jira')
    def test_get_issue_details_success(self, mock_init_jira):
        """Test successful retrieval of issue details."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        
        # Call the function
        result = get_issue_details(self.issue_key)
        
        # Verify JIRA client calls
        mock_init_jira.assert_called_once()
        self.mock_jira.issue.assert_called_once_with(self.issue_key)
        self.mock_jira.transitions.assert_called_once_with(self.mock_issue)
        
        # Verify response structure
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], f'Retrieved details for issue {self.issue_key}')
        
        details = result['details']
        self.assertEqual(details['key'], self.issue_key)
        self.assertEqual(details['summary'], "Test Issue")
        self.assertEqual(details['description'], "Test Description")
        self.assertEqual(details['status'], "In Progress")
        self.assertEqual(details['issue_type'], "Bug")
        self.assertEqual(details['project']['key'], "TEST")
        self.assertEqual(details['project']['name'], "Test Project")
        self.assertEqual(details['creator'], "John Creator")
        self.assertEqual(details['reporter'], "Jane Reporter")
        self.assertEqual(details['assignee'], "Bob Assignee")
        self.assertEqual(details['priority'], "High")
        self.assertEqual(details['labels'], ["bug", "high-priority"])
        self.assertEqual(details['available_transitions'], ["In Progress", "Done"])
        self.assertEqual(
            details['url'],
            f"https://test-jira.atlassian.net/browse/{self.issue_key}"
        )
        
        # Verify comments are not included by default
        self.assertNotIn('comments', details)
        
        logger.info(f"Successfully retrieved details for issue {self.issue_key}")

    @patch('src.tools.issues.initialize_jira')
    def test_get_issue_details_with_comments(self, mock_init_jira):
        """Test retrieval of issue details including comments."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        
        # Call the function with include_comments=True
        result = get_issue_details(self.issue_key, include_comments=True)
        
        # Verify comments are included and correctly formatted
        self.assertIn('comments', result['details'])
        comments = result['details']['comments']
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]['id'], "12345")
        self.assertEqual(comments[0]['body'], "Test comment")
        self.assertEqual(comments[0]['author'], "Comment Author")
        
        logger.info(f"Successfully retrieved issue details with comments for {self.issue_key}")

    @patch('src.tools.issues.initialize_jira')
    def test_get_issue_details_not_found(self, mock_init_jira):
        """Test retrieval of non-existent issue."""
        # Set up mock to return None for non-existent issue
        self.mock_jira.issue.return_value = None
        mock_init_jira.return_value = self.mock_jira
        
        # Verify that attempting to get non-existent issue raises ValueError
        with self.assertRaises(ValueError) as context:
            get_issue_details(self.issue_key)
        
        self.assertEqual(str(context.exception), f"Issue {self.issue_key} not found")
        
        logger.info("Successfully handled non-existent issue request")


if __name__ == '__main__':
    unittest.main() 