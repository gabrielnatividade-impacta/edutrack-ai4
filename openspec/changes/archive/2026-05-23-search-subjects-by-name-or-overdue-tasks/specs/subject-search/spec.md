## ADDED Requirements

### Requirement: Search Subjects by Name
The system SHALL allow authenticated users to search for their subjects by name using a text search query. The search SHALL be case-insensitive and support partial matching.

#### Scenario: User searches by exact subject name
- **WHEN** user calls `GET /subjects/search?name=Mathematics` 
- **THEN** system returns all subjects owned by the user containing "mathematics" (case-insensitive) in their name field

#### Scenario: User searches with partial name
- **WHEN** user calls `GET /subjects/search?name=Math`
- **THEN** system returns all subjects owned by the user with names containing "Math" (e.g., "Mathematics", "Advanced Math", "Math 101")

#### Scenario: User searches with empty name filter
- **WHEN** user calls `GET /subjects/search?name=`
- **THEN** system treats empty name as no name filter and proceeds with other filters (if provided)

### Requirement: Search Subjects by Overdue Task Status
The system SHALL allow authenticated users to filter their subjects to show only those with overdue tasks. A task is considered overdue if its `due_date` is less than the current UTC timestamp.

#### Scenario: User requests subjects with overdue tasks
- **WHEN** user calls `GET /subjects/search?hasOverdueTasks=true`
- **THEN** system returns all subjects owned by the user that have at least one task with `due_date < now()`

#### Scenario: User requests subjects without overdue tasks
- **WHEN** user calls `GET /subjects/search?hasOverdueTasks=false`
- **THEN** system returns all subjects owned by the user that have no tasks with `due_date < now()`

#### Scenario: No subjects have overdue tasks
- **WHEN** user calls `GET /subjects/search?hasOverdueTasks=true` and user has no overdue tasks across any subject
- **THEN** system returns an empty list with zero total count

### Requirement: Combined Search (Name OR Overdue)
The system SHALL allow users to specify both name and overdue task filters simultaneously. Filtering logic SHALL use OR semantics: results include subjects matching either the name filter OR the overdue task filter.

#### Scenario: User searches by both name and overdue status with OR logic
- **WHEN** user calls `GET /subjects/search?name=Math&hasOverdueTasks=true`
- **THEN** system returns all subjects owned by the user that either (a) contain "Math" in their name, or (b) have at least one overdue task, or both

#### Scenario: User provides only one filter
- **WHEN** user calls `GET /subjects/search?name=Physics` (without hasOverdueTasks parameter)
- **THEN** system treats missing filter as "match all" and returns subjects matching the provided filter only

### Requirement: Search Response Includes Task Status Information
The system SHALL return enriched subject data that includes the count of overdue tasks for each subject, allowing users to understand the severity of pending work.

#### Scenario: Subject with overdue tasks returns count
- **WHEN** a subject with 3 overdue tasks is included in search results
- **THEN** the response includes `overdue_task_count: 3` for that subject

#### Scenario: Subject with no overdue tasks
- **WHEN** a subject with no overdue tasks is included in search results
- **THEN** the response includes `overdue_task_count: 0` for that subject

### Requirement: Search Results Include Pagination
The system SHALL support pagination for search results to handle large subject lists efficiently.

#### Scenario: User requests first page of results
- **WHEN** user calls `GET /subjects/search?name=Math&limit=10&offset=0`
- **THEN** system returns up to 10 results, starting from the first matching subject, and includes total count of matching subjects

#### Scenario: User requests subsequent page
- **WHEN** user calls `GET /subjects/search?name=Math&limit=10&offset=10`
- **THEN** system returns subjects 11-20 (if they exist) and includes total count

### Requirement: Authentication and Access Control
The system SHALL enforce that authenticated users can only search and view their own subjects. Unauthenticated requests SHALL be rejected.

#### Scenario: Authenticated user searches their own subjects
- **WHEN** authenticated user with ID 5 calls `/subjects/search?name=Math`
- **THEN** system returns only subjects where `user_id = 5`

#### Scenario: Unauthenticated request is rejected
- **WHEN** request to `/subjects/search` is made without valid authentication token
- **THEN** system returns 401 Unauthorized error

