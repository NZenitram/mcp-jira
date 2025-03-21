#!/usr/bin/env python3
"""Test the JIRA issue transition tool with mocking."""
import unittest
from unittest.mock import patch, MagicMock
import logging
from src.tools.issues import transition_issue

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestTransitionIssue(unittest.TestCase):
    """Test cases for transition_issue using mocks."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.issue_key = "TEST-123"
        self.target_status = "In Progress"
        self.comment = "Transitioning to In Progress"
        
        # Mock issue object and its fields
        self.mock_issue = MagicMock()
        self.mock_issue.key = self.issue_key
        self.mock_fields = MagicMock()
        self.mock_fields.status = MagicMock()
        self.mock_fields.status.name = "Open"  # Initial status
        self.mock_issue.fields = self.mock_fields
        
        # Mock JIRA client
        self.mock_jira = MagicMock()
        self.mock_jira._options = {'server': 'https://test-jira.atlassian.net'}
        self.mock_jira.issue.return_value = self.mock_issue
        
        # Mock available transitions
        self.mock_transitions = [
            {'id': '2', 'name': 'In Progress'},
            {'id': '3', 'name': 'Done'},
            {'id': '4', 'name': 'Blocked'}
        ]
        self.mock_jira.transitions.return_value = self.mock_transitions

    @patch('src.tools.issues.initialize_jira')
    def test_transition_success(self, mock_init_jira):
        """Test successful issue transition."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        
        # Update mock for status after transition
        updated_issue = MagicMock()
        updated_fields = MagicMock()
        updated_fields.status = MagicMock()
        updated_fields.status.name = self.target_status
        updated_issue.fields = updated_fields
        self.mock_jira.issue.side_effect = [self.mock_issue, updated_issue]
        
        # Call the function
        result = transition_issue(self.issue_key, self.target_status, self.comment)
        
        # Verify JIRA client calls
        mock_init_jira.assert_called_once()
        self.mock_jira.transitions.assert_called_once_with(self.mock_issue)
        self.mock_jira.transition_issue.assert_called_once()
        
        # Verify transition data
        transition_call = self.mock_jira.transition_issue.call_args
        self.assertEqual(transition_call[0][0], self.mock_issue)  # First arg is issue
        self.assertEqual(transition_call[0][1], '2')  # Second arg is transition ID
        
        # Verify response structure
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['details']['issue_key'], self.issue_key)
        self.assertEqual(result['details']['previous_status'], 'Open')
        self.assertEqual(result['details']['new_status'], self.target_status)
        self.assertEqual(result['details']['comment_added'], True)
        self.assertEqual(
            result['details']['url'],
            f"https://test-jira.atlassian.net/browse/{self.issue_key}"
        )
        
        logger.info(f"Successfully transitioned issue {self.issue_key} from Open to {self.target_status}")

    @patch('src.tools.issues.initialize_jira')
    def test_transition_invalid_status(self, mock_init_jira):
        """Test transition with invalid target status."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        invalid_status = "Invalid Status"
        
        # Verify that attempting invalid transition raises ValueError
        with self.assertRaises(ValueError) as context:
            transition_issue(self.issue_key, invalid_status)
        
        # Verify error message contains available transitions
        error_msg = str(context.exception)
        self.assertIn(invalid_status, error_msg)
        self.assertIn("Available transitions", error_msg)
        for transition in ['In Progress', 'Done', 'Blocked']:
            self.assertIn(transition, error_msg)
        
        logger.info("Successfully prevented transition to invalid status")

    @patch('src.tools.issues.initialize_jira')
    def test_transition_issue_not_found(self, mock_init_jira):
        """Test transition of non-existent issue."""
        # Set up mock to return None for non-existent issue
        self.mock_jira.issue.return_value = None
        mock_init_jira.return_value = self.mock_jira
        
        # Verify that attempting to transition non-existent issue raises ValueError
        with self.assertRaises(ValueError) as context:
            transition_issue(self.issue_key, self.target_status)
        
        self.assertEqual(str(context.exception), f"Issue {self.issue_key} not found")
        
        logger.info("Successfully prevented transition of non-existent issue")


if __name__ == '__main__':
    unittest.main() 