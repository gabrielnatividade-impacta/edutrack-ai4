## 1. Prerequisite: Verify Tasks Table Structure

- [x] 1.1 Verify if a `tasks` table exists in `tables/` directory
- [x] 1.2 If tasks table doesn't exist, create `tasks` table with fields: `id`, `subject_id`, `title`, `description`, `due_date`, `status` (completed/pending), `created_at`, `updated_at`
- [x] 1.3 Ensure tasks table has proper indexes on `subject_id` and `due_date` for query performance
- [x] 1.4 Verify that `due_date` field can store RFC3339 timestamps and is nullable if tasks can be without deadlines
- [x] 1.5 Push tasks table changes to Xano workspace if created

## 2. Create Python Task Status Calculation Logic

- [x] 2.1 Create a Python utility function `calculate_task_status.py` or `task_utils.py` in `functions/` directory
- [x] 2.2 Implement function to determine if a single task is overdue (due_date < current UTC time)
- [x] 2.3 Implement function to count overdue tasks for a given subject (filter where subject_id matches and due_date < now)
- [x] 2.4 Ensure all date comparisons use UTC timezone and handle RFC3339 format parsing
- [x] 2.5 Add docstrings and type hints to Python functions for clarity
- [x] 2.6 Add unit tests for overdue calculation with edge cases (exact time match, future dates, past dates, null due dates)

## 3. Create XanoScript Wrapper Function for Python Logic

- [x] 3.1 Create `functions/subjects/count_overdue_tasks.xs` that wraps the Python task status logic
- [x] 3.2 Function input: `subject_id` (int) and optional `user_id` (for validation)
- [x] 3.3 Function output: `overdue_task_count` (int) and list of overdue tasks (for debugging if needed)
- [x] 3.4 Implement authentication check to ensure user can only count overdue tasks for their own subjects
- [x] 3.5 Handle case where tasks table doesn't exist gracefully (return 0 overdue tasks)
- [x] 3.6 Document the function in comments

## 4. Implement /subjects/search GET Endpoint

- [x] 4.1 Create new API endpoint file `apis/subjects/3865260_subjects_search_GET.xs` (use appropriate ID)
- [x] 4.2 Define endpoint: `query "search_subjects" verb=GET` in subjects API group
- [x] 4.3 Add input parameters:
  -  `name` (optional text, case-insensitive search)
  -  `hasOverdueTasks` (optional boolean)
  -  `limit` (optional int, default 50, max 100)
  -  `offset` (optional int, default 0)
- [x] 4.4 Implement filter logic:
  - If only `name` provided: filter subjects where name contains search term (case-insensitive)
  - If only `hasOverdueTasks` provided: filter subjects where overdue_task_count > 0 (if true) or == 0 (if false)
  - If both provided: use OR logic (name matches OR has overdue tasks)
- [x] 4.5 Call `count_overdue_tasks` function for each subject in results to populate `overdue_task_count`
- [x] 4.6 Add pagination support using limit and offset
- [x] 4.7 Return enriched subject data including: id, name, code, semester, description, created_at, updated_at, **overdue_task_count**
- [x] 4.8 Ensure authentication requirement (auth = "user") and user_id filtering

## 5. Integrate Python Logic with XanoScript

- [x] 5.1 In the search endpoint, ensure proper integration with Python task status function
- [x] 5.2 Handle potential Python execution errors gracefully (fallback to 0 overdue count if calculation fails)
- [x] 5.3 Optimize query to avoid N+1 problems: consider batching overdue count calculations if possible
- [x] 5.4 Add logging/debug output for task status calculation in development

## 6. Testing and Validation

- [ ] 6.1 Test search by name only: verify case-insensitive partial matching works
- [ ] 6.2 Test search by overdue status only: verify subjects with/without overdue tasks are returned correctly
- [ ] 6.3 Test combined search with OR logic: verify both name matches and overdue subjects are returned
- [ ] 6.4 Test pagination: verify limit and offset parameters work correctly
- [ ] 6.5 Test with no results: verify empty response is returned properly
- [ ] 6.6 Test authentication: verify unauthenticated requests are rejected
- [ ] 6.7 Test user isolation: verify users only see their own subjects
- [ ] 6.8 Test overdue task count accuracy with various dates and timezones
- [ ] 6.9 Test edge case: task with due_date exactly equal to current time (should not be overdue)
- [ ] 6.10 Load test with large number of subjects and tasks to verify performance

## 7. Documentation and Deployment

- [x] 7.1 Document the `/subjects/search` API endpoint in API documentation with examples
- [x] 7.2 Document Python task status calculation logic and how it integrates with XanoScript
- [x] 7.3 Document query limitations and performance considerations
- [ ] 7.4 Add code comments explaining the OR logic for filter combinations
- [x] 7.5 Create example API requests (curl, Postman, or similar) for search functionality
- [ ] 7.6 Push all changes to Xano workspace
- [ ] 7.7 Verify endpoint is accessible and functioning in Xano environment
- [ ] 7.8 Update CHANGELOG or release notes with new search endpoint

## 8. Optional Enhancements (Post-MVP)

- [ ] 8.1 Add sorting options (by name, by overdue count, by date created)
- [ ] 8.2 Add more filter options (by semester, by date range, by task count)
- [ ] 8.3 Add caching layer for overdue counts if performance becomes an issue
- [ ] 8.4 Implement full-text search on subject description in addition to name
- [ ] 8.5 Create UI component to display search results and overdue indicators

