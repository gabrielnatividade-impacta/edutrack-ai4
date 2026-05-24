"""
Unit tests for task_status_utils module.

Tests cover various scenarios:
- Overdue tasks (past due dates)
- Future tasks (not yet due)
- Tasks with exact current time (boundary condition)
- Tasks with no due date (None)
- Invalid date formats
- Multiple tasks with mixed status
"""

import unittest
from datetime import datetime, timezone, timedelta
from task_status_utils import (
    is_task_overdue,
    count_overdue_tasks,
    get_overdue_task_details,
    format_rfc3339_now
)


class TestTaskStatusUtils(unittest.TestCase):
    """Test suite for task status calculation functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.now = datetime.now(timezone.utc)
        self.past = (self.now - timedelta(days=1)).isoformat().replace('+00:00', 'Z')
        self.future = (self.now + timedelta(days=1)).isoformat().replace('+00:00', 'Z')
        self.exact_now = self.now.isoformat().replace('+00:00', 'Z')
    
    # Tests for is_task_overdue
    
    def test_past_due_date_is_overdue(self):
        """Task with past due date should be overdue."""
        self.assertTrue(is_task_overdue(self.past))
    
    def test_future_due_date_not_overdue(self):
        """Task with future due date should not be overdue."""
        self.assertFalse(is_task_overdue(self.future))
    
    def test_exact_current_time_not_overdue(self):
        """Task with due_date equal to current time should not be overdue."""
        # Note: Due to timing precision, we use >= comparisons in actual code
        result = is_task_overdue(self.exact_now)
        # Should be False because < comparison (not <=)
        self.assertFalse(result)
    
    def test_none_due_date_not_overdue(self):
        """Task with None due_date should not be overdue."""
        self.assertFalse(is_task_overdue(None))
    
    def test_invalid_date_format_raises_error(self):
        """Invalid date format should raise ValueError."""
        with self.assertRaises(ValueError):
            is_task_overdue("2024-13-45T25:99:99Z")
    
    def test_empty_date_string_raises_error(self):
        """Empty date string should raise ValueError."""
        with self.assertRaises(ValueError):
            is_task_overdue("")
    
    # Tests for count_overdue_tasks
    
    def test_count_overdue_with_multiple_tasks(self):
        """Count overdue tasks in list with mixed status."""
        tasks = [
            {'id': 1, 'title': 'Task 1', 'due_date': self.past, 'status': 'pending'},
            {'id': 2, 'title': 'Task 2', 'due_date': self.future, 'status': 'pending'},
            {'id': 3, 'title': 'Task 3', 'due_date': self.past, 'status': 'pending'},
        ]
        self.assertEqual(count_overdue_tasks(tasks), 2)
    
    def test_count_ignores_completed_tasks(self):
        """Completed tasks should not count toward overdue."""
        tasks = [
            {'id': 1, 'title': 'Task 1', 'due_date': self.past, 'status': 'pending'},
            {'id': 2, 'title': 'Task 2', 'due_date': self.past, 'status': 'completed'},
        ]
        self.assertEqual(count_overdue_tasks(tasks), 1)
    
    def test_count_empty_list_returns_zero(self):
        """Empty task list should return 0."""
        self.assertEqual(count_overdue_tasks([]), 0)
    
    def test_count_no_overdue_tasks(self):
        """List with no overdue tasks should return 0."""
        tasks = [
            {'id': 1, 'title': 'Task 1', 'due_date': self.future, 'status': 'pending'},
            {'id': 2, 'title': 'Task 2', 'due_date': self.future, 'status': 'pending'},
        ]
        self.assertEqual(count_overdue_tasks(tasks), 0)
    
    def test_count_null_due_dates(self):
        """Tasks with None due_date should not count as overdue."""
        tasks = [
            {'id': 1, 'title': 'Task 1', 'due_date': None, 'status': 'pending'},
            {'id': 2, 'title': 'Task 2', 'due_date': None, 'status': 'pending'},
        ]
        self.assertEqual(count_overdue_tasks(tasks), 0)
    
    # Tests for get_overdue_task_details
    
    def test_get_details_complete_response(self):
        """get_overdue_task_details should return complete information."""
        tasks = [
            {'id': 1, 'title': 'Overdue Task', 'due_date': self.past, 'status': 'pending'},
            {'id': 2, 'title': 'Future Task', 'due_date': self.future, 'status': 'pending'},
            {'id': 3, 'title': 'Completed Overdue', 'due_date': self.past, 'status': 'completed'},
        ]
        result = get_overdue_task_details(tasks)
        
        self.assertEqual(result['count'], 1)
        self.assertEqual(result['pending_count'], 2)
        self.assertEqual(len(result['overdue_tasks']), 1)
        self.assertEqual(result['overdue_tasks'][0]['id'], 1)
    
    def test_get_details_empty_list(self):
        """get_overdue_task_details with empty list should return zeros."""
        result = get_overdue_task_details([])
        
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['pending_count'], 0)
        self.assertEqual(len(result['overdue_tasks']), 0)
    
    # Tests for format_rfc3339_now
    
    def test_format_rfc3339_now_format(self):
        """format_rfc3339_now should return valid RFC3339 format."""
        result = format_rfc3339_now()
        
        # Should end with Z for UTC
        self.assertTrue(result.endswith('Z'))
        # Should be parseable
        try:
            datetime.fromisoformat(result.replace('Z', '+00:00'))
        except ValueError:
            self.fail("format_rfc3339_now returned invalid RFC3339 format")


if __name__ == '__main__':
    unittest.main()
