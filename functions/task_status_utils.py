"""
Task Status Calculation Utility Module

This module provides functions to determine if tasks are overdue and count
overdue tasks for a given subject. All date comparisons are performed in UTC.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional


def is_task_overdue(due_date: Optional[str]) -> bool:
    """
    Determine if a task is overdue by comparing its due date against current UTC time.
    
    A task is overdue if due_date < now(). If due_date is None, the task is not overdue.
    
    Args:
        due_date: Due date in RFC3339 format (e.g., "2024-01-15T10:00:00Z") or None
        
    Returns:
        bool: True if task is overdue, False otherwise
        
    Raises:
        ValueError: If due_date is not in valid RFC3339 format
    """
    if due_date is None:
        return False
    
    try:
        # Parse RFC3339 timestamp
        due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        current_time = datetime.now(timezone.utc).replace(microsecond=0)
        
        # Task is overdue if due date is in the past
        return due_datetime < current_time
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid RFC3339 date format: {due_date}") from e


def count_overdue_tasks(tasks: List[Dict]) -> int:
    """
    Count the number of overdue tasks in a given list of tasks.
    
    Only counts tasks with status != 'completed'. A task is considered overdue
    if its due_date is less than the current UTC timestamp.
    
    Args:
        tasks: List of task dictionaries containing 'due_date' and 'status' keys
        
    Returns:
        int: Count of overdue tasks
    """
    if not tasks:
        return 0
    
    overdue_count = 0
    for task in tasks:
        # Skip completed tasks
        if task.get('status') == 'completed':
            continue
        
        # Check if task is overdue
        due_date = task.get('due_date')
        try:
            if is_task_overdue(due_date):
                overdue_count += 1
        except ValueError:
            # Skip tasks with invalid dates
            continue
    
    return overdue_count


def get_overdue_task_details(tasks: List[Dict]) -> Dict:
    """
    Analyze tasks and return detailed overdue information.
    
    Args:
        tasks: List of task dictionaries containing 'id', 'title', 'due_date', 'status'
        
    Returns:
        dict: {
            'count': int (number of overdue tasks),
            'overdue_tasks': list (details of overdue tasks),
            'pending_count': int (total pending tasks)
        }
    """
    result = {
        'count': 0,
        'overdue_tasks': [],
        'pending_count': 0
    }
    
    if not tasks:
        return result
    
    for task in tasks:
        if task.get('status') != 'completed':
            result['pending_count'] += 1
            
            due_date = task.get('due_date')
            try:
                if is_task_overdue(due_date):
                    result['count'] += 1
                    result['overdue_tasks'].append({
                        'id': task.get('id'),
                        'title': task.get('title'),
                        'due_date': due_date
                    })
            except ValueError:
                continue
    
    return result


def format_rfc3339_now() -> str:
    """
    Get current UTC time in RFC3339 format.
    
    Returns:
        str: Current timestamp in RFC3339 format (e.g., "2024-01-20T09:30:00Z")
    """
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
