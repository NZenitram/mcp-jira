#!/usr/bin/env python3
"""Test the JIRA user search tool with mocking."""
import unittest
from unittest.mock import patch, MagicMock
import logging
from src.tools.issues import search_users

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TestSearchUsers(unittest.TestCase):
    """Test cases for search_users using mocks."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock user attributes
        self.mock_user1 = MagicMock()
        self.mock_user1.accountId = "user123"
        self.mock_user1.displayName = "John Doe"
        self.mock_user1.emailAddress = "john.doe@example.com"
        self.mock_user1.active = True
        self.mock_user1.timeZone = "America/New_York"
        self.mock_user1.locale = "en_US"
        self.mock_user1.avatarUrls = MagicMock()
        self.mock_user1.avatarUrls.__getitem__.return_value = "https://example.com/avatar1.jpg"
        
        self.mock_user2 = MagicMock()
        self.mock_user2.accountId = "user456"
        self.mock_user2.displayName = "Jane Smith"
        self.mock_user2.emailAddress = "jane.smith@example.com"
        self.mock_user2.active = False
        self.mock_user2.timeZone = "Europe/London"
        self.mock_user2.locale = "en_GB"
        self.mock_user2.avatarUrls = MagicMock()
        self.mock_user2.avatarUrls.__getitem__.return_value = "https://example.com/avatar2.jpg"
        
        # Mock JIRA client
        self.mock_jira = MagicMock()
        self.mock_users = [self.mock_user1, self.mock_user2]
        self.mock_jira.search_users.return_value = self.mock_users

    @patch('src.tools.issues.initialize_jira')
    def test_search_users_success(self, mock_init_jira):
        """Test successful user search."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        query = "john"
        
        # Call the function
        result = search_users(query)
        
        # Verify JIRA client calls
        mock_init_jira.assert_called_once()
        self.mock_jira.search_users.assert_called_once_with(
            query,
            maxResults=10,
            includeActive=True,
            includeInactive=False
        )
        
        # Verify response structure
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], f'Found 2 users matching "{query}"')
        
        details = result['details']
        self.assertEqual(details['query'], query)
        self.assertEqual(details['total'], 2)
        self.assertEqual(len(details['users']), 2)
        
        # Verify first user data
        user1 = details['users'][0]
        self.assertEqual(user1['account_id'], "user123")
        self.assertEqual(user1['display_name'], "John Doe")
        self.assertEqual(user1['email'], "john.doe@example.com")
        self.assertEqual(user1['active'], True)
        self.assertEqual(user1['time_zone'], "America/New_York")
        self.assertEqual(user1['locale'], "en_US")
        
        logger.info(f"Successfully searched for users matching '{query}'")

    @patch('src.tools.issues.initialize_jira')
    def test_search_users_with_inactive(self, mock_init_jira):
        """Test user search including inactive users."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        query = "user"
        
        # Call the function with include_inactive_users=True
        result = search_users(query, include_inactive_users=True)
        
        # Verify search parameters
        self.mock_jira.search_users.assert_called_once_with(
            query,
            maxResults=10,
            includeActive=True,
            includeInactive=True
        )
        
        # Verify inactive user is included
        users = result['details']['users']
        inactive_users = [u for u in users if not u['active']]
        self.assertTrue(len(inactive_users) > 0)
        
        logger.info("Successfully included inactive users in search results")

    @patch('src.tools.issues.initialize_jira')
    def test_search_users_empty_query(self, mock_init_jira):
        """Test search with empty query."""
        # Set up mock
        mock_init_jira.return_value = self.mock_jira
        
        # Verify that empty query raises ValueError
        with self.assertRaises(ValueError) as context:
            search_users("")
        
        self.assertEqual(str(context.exception), "Search query cannot be empty")
        
        # Verify JIRA client was not called
        self.mock_jira.search_users.assert_not_called()
        
        logger.info("Successfully handled empty query validation")

    @patch('src.tools.issues.initialize_jira')
    def test_search_users_no_results(self, mock_init_jira):
        """Test search with no matching users."""
        # Set up mock to return empty list
        self.mock_jira.search_users.return_value = []
        mock_init_jira.return_value = self.mock_jira
        query = "nonexistent"
        
        # Call the function
        result = search_users(query)
        
        # Verify response for no results
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], f'Found 0 users matching "{query}"')
        self.assertEqual(result['details']['total'], 0)
        self.assertEqual(len(result['details']['users']), 0)
        
        logger.info("Successfully handled search with no results")


if __name__ == '__main__':
    unittest.main() 