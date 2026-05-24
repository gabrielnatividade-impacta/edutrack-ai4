# Task Status Calculation - Technical Documentation

## Overview

The task status calculation system identifies and counts overdue tasks for academic subjects. It provides a consistent, UTC-based method for determining task urgency and is integrated with the subjects search API.

## Components

### 1. Python Utility Module (`functions/task_status_utils.py`)

Core business logic for overdue task detection, written in Python for testability and clarity.

#### Functions

##### `is_task_overdue(due_date: Optional[str]) -> bool`

Determines if a single task is overdue.

**Parameters:**
- `due_date` (str or None): Due date in RFC3339 format (e.g., "2024-01-15T10:00:00Z")

**Returns:**
- `True`: Task is overdue (due_date < now() in UTC)
- `False`: Task is not overdue or due_date is None

**Example:**
```python
from task_status_utils import is_task_overdue

# Task due 1 day ago → overdue
overdue = is_task_overdue("2024-01-19T10:00:00Z")  # True

# Task due tomorrow → not overdue
not_overdue = is_task_overdue("2024-01-25T10:00:00Z")  # False

# Task with no deadline → not overdue
no_deadline = is_task_overdue(None)  # False
```

##### `count_overdue_tasks(tasks: List[Dict]) -> int`

Counts overdue tasks in a list, ignoring completed tasks.

**Parameters:**
- `tasks`: List of task dictionaries with keys `due_date` and `status`

**Returns:**
- Count of overdue tasks (int)

**Example:**
```python
tasks = [
    {'id': 1, 'due_date': '2024-01-15T10:00:00Z', 'status': 'pending'},
    {'id': 2, 'due_date': '2024-01-25T10:00:00Z', 'status': 'pending'},
    {'id': 3, 'due_date': '2024-01-15T10:00:00Z', 'status': 'completed'},
]

count = count_overdue_tasks(tasks)  # Returns: 1 (only task 1)
```

##### `get_overdue_task_details(tasks: List[Dict]) -> Dict`

Analyzes tasks and returns detailed overdue information.

**Returns:**
```python
{
    'count': int,           # Number of overdue tasks
    'overdue_tasks': [      # List of overdue task details
        {
            'id': int,
            'title': str,
            'due_date': str
        }
    ],
    'pending_count': int    # Total pending tasks (not completed)
}
```

##### `format_rfc3339_now() -> str`

Gets current UTC time in RFC3339 format.

**Returns:**
- Current timestamp as "2024-01-20T09:30:00Z"

### 2. XanoScript Wrapper Function (`functions/subjects/count_overdue_tasks.xs`)

Integrates Python logic with Xano database queries to safely compute overdue task counts.

**Inputs:**
- `subject_id` (int): ID of the subject to analyze
- `user_id` (int, optional): User ID for validation

**Outputs:**
```
{
    "overdue_task_count": int,      // Number of overdue tasks
    "pending_task_count": int,      // Total pending tasks
    "overdue_tasks": [              // Overdue task details (optional)
        {
            "id": int,
            "title": string,
            "due_date": timestamp
        }
    ]
}
```

**Features:**
- ✅ Validates user owns the subject
- ✅ Handles missing tasks table gracefully (returns 0)
- ✅ Counts only pending tasks (ignores completed)
- ✅ UTC timezone consistency
- ✅ Authentication checks

### 3. Integration with Search API

The `/subjects/search` endpoint calls the wrapper function for each subject to populate `overdue_task_count`.

**How it works:**
1. User calls `/subjects/search?hasOverdueTasks=true`
2. API filters subjects by name if provided
3. For each subject, calls `count_overdue_tasks()` function
4. Filters by overdue status if requested
5. Returns enriched subject data with `overdue_task_count`

## Overdue Definition

A task is considered **overdue** when:

```
status != "completed"
AND
due_date IS NOT NULL
AND
due_date < now()  [in UTC]
```

**Key Points:**
- Only "pending" tasks count (completed tasks are ignored)
- Tasks without due dates (NULL) are never overdue
- Comparison is strictly `<`, not `<=` (tasks due exactly now are not overdue)
- All times use UTC timezone

### Examples

| Due Date | Current Time | Status | Overdue? |
|----------|--------------|--------|----------|
| 2024-01-15T10:00:00Z | 2024-01-20T09:00:00Z | pending | ✅ Yes |
| 2024-01-25T10:00:00Z | 2024-01-20T09:00:00Z | pending | ❌ No |
| 2024-01-20T09:00:00Z | 2024-01-20T09:00:00Z | pending | ❌ No |
| 2024-01-15T10:00:00Z | 2024-01-20T09:00:00Z | completed | ❌ No |
| NULL | 2024-01-20T09:00:00Z | pending | ❌ No |

## Date Format Specification

### RFC3339 Format

All dates use RFC3339 (ISO 8601) format:

```
YYYY-MM-DDTHH:MM:SSZ
```

**Examples:**
- `2024-01-20T09:30:00Z` (9:30 AM UTC)
- `2024-12-31T23:59:59Z` (11:59:59 PM UTC on New Year's Eve)
- `2024-01-01T00:00:00Z` (midnight UTC)

**Z suffix** indicates UTC timezone (no offset conversion needed).

### Database Storage

- Store all timestamps as RFC3339 strings or timestamp type with UTC timezone
- Never store times in local timezone
- Xano's `timestamp` type automatically uses UTC

### Python Parsing

```python
from datetime import datetime, timezone

# Parse RFC3339 timestamp
due_date_str = "2024-01-15T10:00:00Z"
due_datetime = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
# Result: datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

# Compare with now
now = datetime.now(timezone.utc)
is_overdue = due_datetime < now
```

## Performance Considerations

### Database Indexes

The tasks table should have indexes on:
- `subject_id` (filter by subject)
- `due_date` (filter overdue)
- `(subject_id, due_date)` (composite index for common query pattern)
- `status` (filter pending)

### Query Optimization

**Current approach:**
1. Fetch all subjects matching name filter
2. For each subject, query tasks and count overdue
3. Filter results by overdue status (if requested)

**Potential optimizations (future):**
- Batch overdue counting in a single database query
- Cache overdue counts with TTL (if real-time accuracy not critical)
- Denormalize subject_overdue_count field

### Scalability

**Current limitations:**
- API endpoint performs N+1 queries (1 subjects query + 1 task query per subject)
- Suitable for typical user workloads (≤100 subjects)
- May need optimization for users with 1000+ subjects

**Recommendations:**
- Use pagination (limit=10-50) for reasonable response times
- Monitor query performance with logging
- Consider database-level aggregation for large datasets

## Testing

Unit tests are provided in `functions/test_task_status_utils.py`.

### Test Coverage

- ✅ Past due dates (overdue)
- ✅ Future due dates (not overdue)
- ✅ Exact current time (not overdue)
- ✅ NULL due dates (not overdue)
- ✅ Invalid date formats (error handling)
- ✅ Mixed task statuses (completed ignored)
- ✅ Empty task lists
- ✅ Multiple overdue tasks

### Running Tests

```bash
cd functions
python -m pytest test_task_status_utils.py -v
```

Or with unittest:

```bash
python -m unittest test_task_status_utils.py
```

## Error Handling

### Invalid Date Formats

If a task has an invalid RFC3339 date:
- Python functions raise `ValueError`
- XanoScript wrapper gracefully returns 0 for that task
- API endpoint continues processing other tasks

**Example:**
```python
is_task_overdue("2024-13-45")  # Raises ValueError
# Caught and task skipped in count_overdue_tasks()
```

### Missing Tasks Table

If the tasks table doesn't exist:
- Wrapper function catches error and returns `overdue_task_count: 0`
- API endpoint continues normal operation
- No failures propagated to client

### User Authorization

- Wrapper function verifies user owns the subject
- Unauthorized users get `overdue_task_count: 0`
- API endpoint doesn't expose subjects belonging to other users

## Integration Checklist

Before deploying:

- [ ] Tasks table created with `due_date` field (nullable timestamp)
- [ ] Python module (`task_status_utils.py`) created and tested
- [ ] XanoScript wrapper function (`count_overdue_tasks.xs`) deployed
- [ ] API endpoint (`/subjects/search`) deployed
- [ ] Indexes created on tasks table (subject_id, due_date)
- [ ] API documentation available to users
- [ ] Error logging enabled in Xano environment

## Future Enhancements

### Planned Features

1. **Task Priority Levels**: Add severity beyond just overdue/pending
2. **Recurring Tasks**: Support recurring task patterns
3. **Task Categories**: Group tasks and filter by category
4. **Smart Notifications**: Alert users when task becomes overdue
5. **Analytics**: Track task completion rates per subject

### Performance Optimizations

1. **Aggregation Query**: Single database query for overdue counts
2. **Caching Layer**: Cache results with TTL for frequently accessed subjects
3. **Full-Text Search**: Enhance name matching with fuzzy search

## Support & Troubleshooting

### Common Issues

**Q: Task is due in the future but showing as overdue**
- Check timezone: ensure task due_date is in UTC
- Check current server time synchronization
- Verify RFC3339 format is correct

**Q: Deleted completed tasks still counted**
- Completed tasks are excluded by status check, not deletion
- If needed to exclude, check database for `status = 'completed'`

**Q: API slow with many subjects**
- Enable pagination (use limit parameter)
- Check task table indexes exist
- Consider caching or optimization strategies

### Debug Logging

Enable debug mode in Xano to see:
- SQL queries executed
- Task status calculations
- Overdue count results

