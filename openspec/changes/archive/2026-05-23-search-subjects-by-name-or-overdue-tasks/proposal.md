## Why

Currently, users can list all their subjects with optional pagination and semester filtering, but lack an efficient way to search for subjects by name or identify subjects that have overdue tasks. This creates friction when students need to quickly find specific subjects or prioritize those with pending assignments, especially in a context where many subjects exist simultaneously.

## What Changes

- **New Search Endpoint**: Create a dedicated search endpoint (`/subjects/search`) that supports filtering by:
  - Subject name (text search, case-insensitive partial match)
  - Overdue tasks indicator (boolean flag to return only subjects with past-due tasks)
  - Combination of both filters (OR logic between name and overdue status)
- **Python Integration Layer**: Implement Python-based logic to calculate and identify overdue tasks by checking task due dates against the current timestamp
- **Enhanced Data Response**: Return enriched subject data including task status information and overdue task counts
- **Maintain Backward Compatibility**: Keep existing `/subjects` endpoint unchanged

## Capabilities

### New Capabilities

- `subject-search`: New search endpoint with name and overdue task filtering capabilities
- `task-status-calculation`: Python-based logic to identify and calculate overdue task status for subjects

### Modified Capabilities

- `subject-management`: Extend existing subject retrieval to support enriched data with task status information (no breaking changes to current endpoints)

## Impact

- **New API Endpoint**: `/subjects/search` (GET) in the subjects API group
- **New Python Module**: Task status calculation logic (can be integrated as a function or external service)
- **Data Structure**: May require a tasks table structure (if not yet created) to store task information and due dates
- **Backend**: XanoScript API endpoints and potentially Python utility functions
- **Frontend**: New UI components to leverage the search capability (out of scope for this change)

