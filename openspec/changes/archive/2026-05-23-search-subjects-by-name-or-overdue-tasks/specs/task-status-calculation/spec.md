## ADDED Requirements

### Requirement: Calculate Task Overdue Status
The system SHALL determine whether a task is overdue by comparing its due date against the current UTC timestamp. A task is overdue if `due_date < now()` in UTC timezone.

#### Scenario: Task with past due date is identified as overdue
- **WHEN** a task has `due_date = 2024-01-15 10:00:00 UTC` and current time is `2024-01-20 09:00:00 UTC`
- **THEN** the system identifies this task as overdue

#### Scenario: Task with future due date is not overdue
- **WHEN** a task has `due_date = 2024-01-25 10:00:00 UTC` and current time is `2024-01-20 09:00:00 UTC`
- **THEN** the system does not identify this task as overdue

#### Scenario: Task with due date equal to current time is not overdue
- **WHEN** a task has `due_date = 2024-01-20 09:00:00 UTC` and current time is exactly `2024-01-20 09:00:00 UTC`
- **THEN** the system does not identify this task as overdue (equality is not "less than")

### Requirement: Count Overdue Tasks Per Subject
The system SHALL compute the count of overdue tasks for each subject owned by the authenticated user. This count enables users to prioritize subjects by workload urgency.

#### Scenario: Subject with multiple overdue tasks
- **WHEN** a subject has 5 total tasks, 3 of which are overdue
- **THEN** the system returns `overdue_task_count = 3` for that subject

#### Scenario: Subject with no tasks
- **WHEN** a subject has no associated tasks
- **THEN** the system returns `overdue_task_count = 0` for that subject

#### Scenario: Subject with all tasks completed (no pending overdue)
- **WHEN** a subject has 5 completed tasks and 0 pending tasks
- **THEN** the system returns `overdue_task_count = 0` for that subject

### Requirement: Task Status Calculation is Real-Time
The system SHALL calculate task overdue status at query time using the current timestamp, ensuring results always reflect the current state without requiring background jobs or cache invalidation.

#### Scenario: Status changes as time progresses
- **WHEN** a task with `due_date = 2024-01-20 10:00:00 UTC` is queried at `2024-01-20 09:30:00 UTC`
- **THEN** system returns `overdue = false`
- **WHEN** the same task is queried again at `2024-01-20 10:30:00 UTC` (after due date has passed)
- **THEN** system returns `overdue = true`

### Requirement: Python-Based Status Calculation Logic
The system SHALL implement task status calculation using Python logic that can be called from XanoScript API endpoints. The Python implementation SHALL handle date comparisons and UTC timestamp conversions consistently.

#### Scenario: Python function validates overdue status
- **WHEN** a Python utility function is called with `task_due_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)` and `current_time = datetime(2024, 1, 20, 9, 0, 0, tzinfo=UTC)`
- **THEN** the function returns `is_overdue = True`

#### Scenario: Python function handles timezone-aware datetimes
- **WHEN** the Python function receives due dates in RFC3339 format (e.g., "2024-01-15T10:00:00Z")
- **THEN** the function correctly parses them to UTC and compares against current time without timezone conversion errors

### Requirement: Integration with Subject Search Results
The system SHALL integrate task status calculation with the subject search feature, returning the overdue task count in search response payloads so users see urgency indicators.

#### Scenario: Search results include overdue task counts
- **WHEN** a user calls `/subjects/search?name=Math`
- **THEN** each subject in the results includes `overdue_task_count: <number>` field populated by the status calculation logic

#### Scenario: Overdue count updates across multiple searches
- **WHEN** a user runs two consecutive searches with the same filters
- **THEN** each search independently calculates current overdue status, reflecting any new due dates that have passed in between searches

