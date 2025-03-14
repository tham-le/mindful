import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app
from models import User, Transaction, Budget, SavedImpulse

class TestDashboardAPI(unittest.TestCase):
    """Test cases for the dashboard API endpoints"""

    def setUp(self):
        """Set up test environment"""
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        # Create a mock user
        self.mock_user = MagicMock(spec=User)
        self.mock_user.id = 1
        self.mock_user.name = "Test User"
        self.mock_user.email = "test@example.com"
        
        # Create a mock JWT token
        self.mock_token = "mock_token"
        
        # Create a patch for the get_current_user function
        self.get_current_user_patcher = patch('app.get_current_user')
        self.mock_get_current_user = self.get_current_user_patcher.start()
        self.mock_get_current_user.return_value = self.mock_user
        
        # Create a patch for the jwt_required decorator
        self.jwt_required_patcher = patch('app.jwt_required')
        self.mock_jwt_required = self.jwt_required_patcher.start()
        
        # Create a patch for the db_session
        self.db_session_patcher = patch('app.db_session')
        self.mock_db_session = self.db_session_patcher.start()
        
        # Create mock query results
        self.mock_transactions = [
            MagicMock(spec=Transaction),
            MagicMock(spec=Transaction)
        ]
        self.mock_transactions[0].id = 1
        self.mock_transactions[0].user_id = 1
        self.mock_transactions[0].amount = 100.0
        self.mock_transactions[0].category = "groceries"
        self.mock_transactions[0].date = "2023-01-01"
        self.mock_transactions[0].description = "Grocery shopping"
        self.mock_transactions[0].is_impulse = False
        self.mock_transactions[0].to_dict.return_value = {
            "id": 1,
            "user_id": 1,
            "amount": 100.0,
            "category": "groceries",
            "date": "2023-01-01",
            "description": "Grocery shopping",
            "is_impulse": False
        }
        
        self.mock_transactions[1].id = 2
        self.mock_transactions[1].user_id = 1
        self.mock_transactions[1].amount = 200.0
        self.mock_transactions[1].category = "entertainment"
        self.mock_transactions[1].date = "2023-01-02"
        self.mock_transactions[1].description = "Movie tickets"
        self.mock_transactions[1].is_impulse = True
        self.mock_transactions[1].to_dict.return_value = {
            "id": 2,
            "user_id": 1,
            "amount": 200.0,
            "category": "entertainment",
            "date": "2023-01-02",
            "description": "Movie tickets",
            "is_impulse": True
        }
        
        self.mock_budgets = [
            MagicMock(spec=Budget),
            MagicMock(spec=Budget)
        ]
        self.mock_budgets[0].id = 1
        self.mock_budgets[0].user_id = 1
        self.mock_budgets[0].category = "groceries"
        self.mock_budgets[0].planned_amount = 500.0
        self.mock_budgets[0].month = 1
        self.mock_budgets[0].year = 2023
        
        self.mock_budgets[1].id = 2
        self.mock_budgets[1].user_id = 1
        self.mock_budgets[1].category = "entertainment"
        self.mock_budgets[1].planned_amount = 300.0
        self.mock_budgets[1].month = 1
        self.mock_budgets[1].year = 2023
        
        self.mock_impulses = [
            MagicMock(spec=SavedImpulse),
            MagicMock(spec=SavedImpulse)
        ]
        self.mock_impulses[0].id = 1
        self.mock_impulses[0].user_id = 1
        self.mock_impulses[0].description = "Designer shoes"
        self.mock_impulses[0].category = "clothing"
        self.mock_impulses[0].amount = 300.0
        self.mock_impulses[0].date = "2023-01-03"
        self.mock_impulses[0].projected_value_1yr = 324.0
        self.mock_impulses[0].projected_value_5yr = 440.0
        self.mock_impulses[0].to_dict.return_value = {
            "id": 1,
            "user_id": 1,
            "description": "Designer shoes",
            "category": "clothing",
            "amount": 300.0,
            "date": "2023-01-03",
            "projected_value_1yr": 324.0,
            "projected_value_5yr": 440.0
        }
        
        self.mock_impulses[1].id = 2
        self.mock_impulses[1].user_id = 1
        self.mock_impulses[1].description = "Smart watch"
        self.mock_impulses[1].category = "electronics"
        self.mock_impulses[1].amount = 400.0
        self.mock_impulses[1].date = "2023-01-04"
        self.mock_impulses[1].projected_value_1yr = 432.0
        self.mock_impulses[1].projected_value_5yr = 587.0
        self.mock_impulses[1].to_dict.return_value = {
            "id": 2,
            "user_id": 1,
            "description": "Smart watch",
            "category": "electronics",
            "amount": 400.0,
            "date": "2023-01-04",
            "projected_value_1yr": 432.0,
            "projected_value_5yr": 587.0
        }
        
        # Set up mock query results
        self.mock_query = MagicMock()
        self.mock_db_session.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_query
        self.mock_query.filter_by.return_value = self.mock_query
        self.mock_query.all.return_value = self.mock_transactions
        
    def tearDown(self):
        """Clean up after tests"""
        self.get_current_user_patcher.stop()
        self.jwt_required_patcher.stop()
        self.db_session_patcher.stop()

    def test_dashboard_endpoint(self):
        """Test the /api/dashboard endpoint"""
        # Set up mock query results for different queries
        mock_query_transaction = MagicMock()
        mock_query_budget = MagicMock()
        mock_query_impulse = MagicMock()
        
        self.mock_db_session.query.side_effect = [
            mock_query_transaction,  # For Transaction query
            mock_query_transaction,  # For previous month Transaction query
            mock_query_transaction,  # For all transactions query
            mock_query_budget,       # For Budget query
            mock_query_impulse       # For SavedImpulse query
        ]
        
        mock_query_transaction.filter.return_value = mock_query_transaction
        mock_query_transaction.filter_by.return_value = mock_query_transaction
        mock_query_transaction.order_by.return_value = mock_query_transaction
        mock_query_transaction.all.side_effect = [
            self.mock_transactions,  # Current month transactions
            [],                      # Previous month transactions
            self.mock_transactions   # All transactions
        ]
        
        mock_query_budget.filter_by.return_value = mock_query_budget
        mock_query_budget.all.return_value = self.mock_budgets
        
        mock_query_impulse.filter_by.return_value = mock_query_impulse
        mock_query_impulse.all.return_value = self.mock_impulses
        
        # Make the request
        response = self.client.get('/api/dashboard')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('summary', data)
        self.assertIn('categories', data)
        self.assertIn('portfolio', data)
        self.assertIn('activity', data)
        self.assertIn('goals', data)
        self.assertIn('insights', data)
        
        # Check the summary data
        summary = data['summary']
        self.assertIn('total_spent', summary)
        self.assertIn('total_budget', summary)
        self.assertIn('budget_remaining', summary)
        self.assertIn('total_saved', summary)
        self.assertIn('total_balance', summary)
        self.assertIn('monthly_income', summary)
        self.assertIn('monthly_expenses', summary)
        self.assertIn('savingsRate', summary)
        
        # Check the portfolio data
        portfolio = data['portfolio']
        self.assertIn('total', portfolio)
        self.assertIn('allocation', portfolio)
        
        # Check the goals data
        goals = data['goals']
        self.assertEqual(len(goals), 3)  # Should have 3 goals
        for goal in goals:
            self.assertIn('name', goal)
            self.assertIn('current', goal)
            self.assertIn('target', goal)
            self.assertIn('progress', goal)
        
        # Check the insights data
        insights = data['insights']
        self.assertGreater(len(insights), 0)  # Should have at least one insight
        for insight in insights:
            self.assertIn('type', insight)
            self.assertIn('title', insight)
            self.assertIn('description', insight)

    def test_goals_endpoint(self):
        """Test the /api/goals endpoint"""
        # Set up mock query results
        mock_query = MagicMock()
        self.mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.all.return_value = self.mock_impulses
        
        # Make the request
        response = self.client.get('/api/goals')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertEqual(len(data), 3)  # Should have 3 goals
        for goal in data:
            self.assertIn('name', goal)
            self.assertIn('current', goal)
            self.assertIn('target', goal)
            self.assertIn('progress', goal)

    def test_portfolio_endpoint(self):
        """Test the /api/portfolio endpoint"""
        # Set up mock query results
        mock_query = MagicMock()
        self.mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.all.return_value = self.mock_impulses
        
        # Make the request
        response = self.client.get('/api/portfolio')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('total', data)
        self.assertIn('allocation', data)
        self.assertIn('performance', data)
        
        # Check the allocation data
        allocation = data['allocation']
        self.assertIn('stocks', allocation)
        self.assertIn('bonds', allocation)
        self.assertIn('cash', allocation)
        
        # Check the performance data
        performance = data['performance']
        self.assertIn('ytd', performance)
        self.assertIn('oneYear', performance)
        self.assertIn('threeYears', performance)

    def test_activity_endpoint(self):
        """Test the /api/activity endpoint"""
        # Set up mock query results for transactions
        mock_query_transaction = MagicMock()
        self.mock_db_session.query.side_effect = [
            mock_query_transaction,  # For Transaction query
            mock_query_transaction   # For SavedImpulse query
        ]
        
        mock_query_transaction.filter_by.return_value = mock_query_transaction
        mock_query_transaction.order_by.return_value = mock_query_transaction
        mock_query_transaction.limit.return_value = mock_query_transaction
        mock_query_transaction.all.side_effect = [
            self.mock_transactions,  # Transactions
            self.mock_impulses       # Saved impulses
        ]
        
        # Make the request
        response = self.client.get('/api/activity')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertEqual(len(data), 4)  # Should have 4 activities (2 transactions + 2 impulses)
        for activity in data:
            self.assertIn('id', activity)
            self.assertIn('title', activity)
            self.assertIn('time', activity)
            self.assertIn('amount', activity)
            self.assertIn('type', activity)

    def test_insights_endpoint(self):
        """Test the /api/insights endpoint"""
        # Set up mock query results
        mock_query_transaction = MagicMock()
        mock_query_budget = MagicMock()
        mock_query_impulse = MagicMock()
        
        self.mock_db_session.query.side_effect = [
            mock_query_transaction,  # For Transaction query
            mock_query_budget,       # For Budget query
            mock_query_impulse       # For SavedImpulse query
        ]
        
        mock_query_transaction.filter.return_value = mock_query_transaction
        mock_query_transaction.filter_by.return_value = mock_query_transaction
        mock_query_transaction.all.return_value = self.mock_transactions
        
        mock_query_budget.filter_by.return_value = mock_query_budget
        mock_query_budget.all.return_value = self.mock_budgets
        
        mock_query_impulse.filter_by.return_value = mock_query_impulse
        mock_query_impulse.all.return_value = self.mock_impulses
        
        # Make the request
        response = self.client.get('/api/insights')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertGreater(len(data), 0)  # Should have at least one insight
        for insight in data:
            self.assertIn('type', insight)
            self.assertIn('title', insight)
            self.assertIn('description', insight)

if __name__ == '__main__':
    unittest.main() 