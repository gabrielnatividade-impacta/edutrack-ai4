# Subjects Search API Documentation

## Endpoint: GET /subjects/search

Search and filter your academic subjects by name and/or overdue task status. Results are enriched with overdue task counts to help prioritize work.

### Authentication
**Required:** Yes (User authentication required)

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | string | No | - | Subject name search term (case-insensitive, partial matching) |
| `hasOverdueTasks` | boolean | No | - | Filter by overdue task status: `true` to show only subjects with overdue tasks, `false` to show only subjects without overdue tasks |
| `limit` | integer | No | 50 | Maximum number of results to return (1-100) |
| `offset` | integer | No | 0 | Number of results to skip for pagination (≥ 0) |

### Query Examples

#### 1. Search by Subject Name Only
```
GET /subjects/search?name=Mathematics
```
Returns all subjects containing "Mathematics" in the name (case-insensitive).

#### 2. Filter by Overdue Tasks Only
```
GET /subjects/search?hasOverdueTasks=true
```
Returns all subjects that have at least one pending task with `due_date < now()`.

#### 3. Combined Search (OR Logic)
```
GET /subjects/search?name=Math&hasOverdueTasks=true
```
Returns subjects that either:
- Contain "Math" in their name, OR
- Have at least one overdue task

#### 4. Pagination
```
GET /subjects/search?name=Math&limit=10&offset=20
```
Returns results 21-30 for subjects matching "Math".

### Response Format

#### Success Response (HTTP 200)
```json
{
  "type": "list",
  "paging": {
    "count": 5,
    "total_count": 5
  },
  "data": [
    {
      "id": 1,
      "name": "Advanced Mathematics",
      "code": "MATH401",
      "semester": "Spring 2024",
      "description": "Calculus and linear algebra",
      "created_at": "2024-01-15T08:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z",
      "overdue_task_count": 2,
      "pending_task_count": 5
    },
    {
      "id": 3,
      "name": "Physics I",
      "code": "PHYS101",
      "semester": "Spring 2024",
      "description": "Introduction to classical mechanics",
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-19T09:15:00Z",
      "overdue_task_count": 0,
      "pending_task_count": 2
    }
  ]
}
```

#### Empty Results (HTTP 200)
```json
{
  "type": "list",
  "paging": {
    "count": 0,
    "total_count": 0
  },
  "data": []
}
```

#### Unauthorized (HTTP 401)
```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always "list" |
| `paging.count` | integer | Number of results in this response |
| `paging.total_count` | integer | Total number of matching results |
| `data` | array | Array of subject objects |
| `data[].id` | integer | Subject ID |
| `data[].name` | string | Subject name |
| `data[].code` | string | Subject code (unique per user) |
| `data[].semester` | string | Academic semester/period |
| `data[].description` | string | Optional subject description |
| `data[].created_at` | timestamp | Creation timestamp (RFC3339) |
| `data[].updated_at` | timestamp | Last update timestamp (RFC3339) |
| `data[].overdue_task_count` | integer | Number of pending tasks with due_date < now() |
| `data[].pending_task_count` | integer | Total number of pending (uncompleted) tasks |

### Filter Logic

#### Name Filter
- **Case-insensitive**: "math" matches "Mathematics", "MATH", "Math"
- **Partial matching**: "math" matches "Advanced Mathematics", "Mathematics 101"
- **Empty string**: Treated as no filter

#### Overdue Task Filter
- **true**: Returns only subjects with `overdue_task_count > 0`
- **false**: Returns only subjects with `overdue_task_count == 0`
- **null/omitted**: No filter applied (all subjects included)

#### Combined Filters (OR Logic)
When both `name` and `hasOverdueTasks` are provided:
```
Include subject if:
  (name matches) OR (has overdue tasks)
```

Example:
- Search: `?name=Physics&hasOverdueTasks=true`
- Results: Subjects with "Physics" in name PLUS subjects with overdue tasks (including non-Physics subjects)

### Pagination

- **Limit**: Controls page size (1-100, default 50)
- **Offset**: Controls which page (0-based, default 0)
- **Total Count**: Always returned to help with pagination UI

### Important Notes

#### Overdue Task Definition
A task is considered **overdue** if:
1. Status is "pending" (not "completed")
2. `due_date` is not null
3. `due_date < current_time` (in UTC)

#### Performance Considerations
- Search results are limited to 100 subjects per page to maintain performance
- Overdue task count is calculated in real-time, ensuring accuracy
- For large subject lists, use pagination with reasonable limits
- Indexed fields (subject name, due dates) enable efficient searching

#### UTC Timezone
- All timestamps use UTC timezone (RFC3339 format with Z suffix)
- Overdue calculations compare against current UTC time
- No timezone conversion is performed; ensure due dates are stored in UTC

### Example Use Cases

#### 1. Find Critical Subjects
```
GET /subjects/search?hasOverdueTasks=true
```
Shows subjects that need immediate attention due to overdue tasks.

#### 2. Find Specific Subject
```
GET /subjects/search?name=Chemistry
```
Quickly locate the Chemistry subject even if exact name is unknown.

#### 3. Find Urgent Physics Classes
```
GET /subjects/search?name=Physics&hasOverdueTasks=true
```
Find Physics subjects with overdue work.

#### 4. Browse with Pagination
```
GET /subjects/search?limit=10&offset=0
```
Load first 10 subjects (then use offset=10 for next page).

### Error Handling

#### Invalid Parameters
- Limit > 100: Returns error "Limit must be ≤ 100"
- Limit < 1: Returns error "Limit must be ≥ 1"
- Offset < 0: Returns error "Offset must be ≥ 0"

#### Access Control
- Users can only search and view their own subjects
- Attempting to search will only return authenticated user's subjects

### Integration with Task Management

This endpoint is designed to integrate with a task management system:
1. Each subject can have multiple pending tasks
2. Tasks have a `due_date` field (nullable)
3. Task status can be "pending" or "completed"
4. Overdue count helps users prioritize

For task management endpoints, see the Tasks API documentation.

