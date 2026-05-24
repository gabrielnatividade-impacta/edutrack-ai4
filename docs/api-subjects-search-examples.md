# Subjects Search - Example API Requests

Collection of example requests for the `/subjects/search` endpoint in different formats.

## cURL Examples

### Search by Subject Name

```bash
# Find all subjects containing "Mathematics"
curl -X GET "https://your-xano-domain.com/subjects/search?name=Mathematics" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Search by Overdue Tasks

```bash
# Find all subjects with overdue tasks
curl -X GET "https://your-xano-domain.com/subjects/search?hasOverdueTasks=true" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Combined Search with Pagination

```bash
# Find subjects matching "Physics" OR with overdue tasks, get 10 results
curl -X GET "https://your-xano-domain.com/subjects/search?name=Physics&hasOverdueTasks=true&limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

### Pagination - Next Page

```bash
# Get next 10 results (skip first 10)
curl -X GET "https://your-xano-domain.com/subjects/search?name=Math&limit=10&offset=10" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

## JavaScript/Fetch Examples

### Basic Search

```javascript
const authToken = 'YOUR_AUTH_TOKEN';

// Search for subjects by name
async function searchSubjects(name) {
  const response = await fetch(
    `/subjects/search?name=${encodeURIComponent(name)}`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  const data = await response.json();
  return data;
}

// Usage
searchSubjects('Mathematics').then(data => {
  console.log(`Found ${data.paging.count} subjects`);
  data.data.forEach(subject => {
    console.log(`${subject.name} (${subject.overdue_task_count} overdue)`);
  });
});
```

### Combined Search with Async/Await

```javascript
async function findUrgentSubjects() {
  const params = new URLSearchParams({
    name: 'Math',
    hasOverdueTasks: true,
    limit: 20,
    offset: 0
  });
  
  try {
    const response = await fetch(`/subjects/search?${params}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('Search failed:', error);
    return [];
  }
}

// Usage
const urgentSubjects = await findUrgentSubjects();
```

### Pagination with Loop

```javascript
async function getAllSubjects(pageSize = 50) {
  let allSubjects = [];
  let offset = 0;
  let hasMore = true;
  
  while (hasMore) {
    const params = new URLSearchParams({
      limit: pageSize,
      offset: offset
    });
    
    const response = await fetch(`/subjects/search?${params}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    allSubjects = allSubjects.concat(data.data);
    
    hasMore = data.paging.count === pageSize;
    offset += pageSize;
  }
  
  return allSubjects;
}
```

## Python Examples

### Simple Request

```python
import requests

auth_token = 'YOUR_AUTH_TOKEN'
base_url = 'https://your-xano-domain.com'

def search_subjects(name=None, has_overdue=None, limit=50, offset=0):
    """Search subjects with optional filters."""
    params = {
        'limit': limit,
        'offset': offset
    }
    
    if name:
        params['name'] = name
    
    if has_overdue is not None:
        params['hasOverdueTasks'] = has_overdue
    
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f'{base_url}/subjects/search',
        params=params,
        headers=headers
    )
    
    return response.json()

# Usage
result = search_subjects(name='Mathematics')
print(f"Found {result['paging']['count']} subjects")
for subject in result['data']:
    print(f"{subject['name']}: {subject['overdue_task_count']} overdue tasks")
```

### Find Urgent Work

```python
def find_subjects_with_urgent_work(auth_token, base_url):
    """Get all subjects with overdue tasks."""
    response = requests.get(
        f'{base_url}/subjects/search',
        params={'hasOverdueTasks': True},
        headers={
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
    )
    
    data = response.json()
    
    # Sort by number of overdue tasks (most urgent first)
    sorted_subjects = sorted(
        data['data'],
        key=lambda x: x['overdue_task_count'],
        reverse=True
    )
    
    return sorted_subjects

# Usage
urgent = find_subjects_with_urgent_work(auth_token, base_url)
print(f"You have {len(urgent)} subjects with overdue work:")
for subject in urgent:
    print(f"  - {subject['name']}: {subject['overdue_task_count']} overdue")
```

## Postman Collection Example

Import this as a Postman collection:

```json
{
  "info": {
    "name": "Subjects Search API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{AUTH_TOKEN}}",
        "type": "string"
      }
    ]
  },
  "item": [
    {
      "name": "Search by Name",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{BASE_URL}}/subjects/search?name=Mathematics&limit=50&offset=0",
          "host": ["{{BASE_URL}}"],
          "path": ["subjects", "search"],
          "query": [
            {"key": "name", "value": "Mathematics"},
            {"key": "limit", "value": "50"},
            {"key": "offset", "value": "0"}
          ]
        }
      }
    },
    {
      "name": "Search by Overdue Tasks",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{BASE_URL}}/subjects/search?hasOverdueTasks=true&limit=50&offset=0",
          "host": ["{{BASE_URL}}"],
          "path": ["subjects", "search"],
          "query": [
            {"key": "hasOverdueTasks", "value": "true"},
            {"key": "limit", "value": "50"},
            {"key": "offset", "value": "0"}
          ]
        }
      }
    },
    {
      "name": "Combined Search (OR Logic)",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{BASE_URL}}/subjects/search?name=Physics&hasOverdueTasks=true&limit=50&offset=0",
          "host": ["{{BASE_URL}}"],
          "path": ["subjects", "search"],
          "query": [
            {"key": "name", "value": "Physics"},
            {"key": "hasOverdueTasks", "value": "true"},
            {"key": "limit", "value": "50"},
            {"key": "offset", "value": "0"}
          ]
        }
      }
    }
  ]
}
```

### Postman Variables

In Postman, set these variables:
- `BASE_URL`: https://your-xano-domain.com
- `AUTH_TOKEN`: Your authentication token

## Response Examples

### Example 1: Search with Results

Request:
```
GET /subjects/search?name=Math
```

Response (HTTP 200):
```json
{
  "type": "list",
  "paging": {
    "count": 2,
    "total_count": 2
  },
  "data": [
    {
      "id": 1,
      "name": "Advanced Mathematics",
      "code": "MATH401",
      "semester": "Spring 2024",
      "description": "Calculus and linear algebra advanced topics",
      "created_at": "2024-01-15T08:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z",
      "overdue_task_count": 2,
      "pending_task_count": 5
    },
    {
      "id": 4,
      "name": "Discrete Mathematics",
      "code": "MATH220",
      "semester": "Spring 2024",
      "description": "Logic, sets, graphs, and proofs",
      "created_at": "2024-01-12T10:15:00Z",
      "updated_at": "2024-01-18T16:45:00Z",
      "overdue_task_count": 0,
      "pending_task_count": 3
    }
  ]
}
```

### Example 2: No Results

Request:
```
GET /subjects/search?name=NonExistent
```

Response (HTTP 200):
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

### Example 3: Overdue Subjects

Request:
```
GET /subjects/search?hasOverdueTasks=true
```

Response (HTTP 200):
```json
{
  "type": "list",
  "paging": {
    "count": 1,
    "total_count": 1
  },
  "data": [
    {
      "id": 1,
      "name": "Advanced Mathematics",
      "code": "MATH401",
      "semester": "Spring 2024",
      "description": "Calculus and linear algebra advanced topics",
      "created_at": "2024-01-15T08:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z",
      "overdue_task_count": 2,
      "pending_task_count": 5
    }
  ]
}
```

### Example 4: Unauthorized

Request (without authentication):
```
GET /subjects/search
```

Response (HTTP 401):
```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

