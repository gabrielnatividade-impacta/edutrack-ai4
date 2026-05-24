## Context

The EduTrack AI system manages academic subjects for authenticated users. Currently:
- Subjects are stored in the `subjects` table with basic metadata (name, code, semester, description)
- The existing GET `/subjects` endpoint provides list retrieval with pagination and semester filtering
- There is no task/assignment management table in the current system
- The system uses XanoScript for API endpoints and could leverage Python for complex business logic

Users need an efficient way to find subjects by name or identify which subjects have overdue tasks, but:
- No tasks table exists yet in the data model
- Search functionality is limited to basic pagination and semester filters
- There is no task deadline tracking or overdue status calculation

## Goals / Non-Goals

**Goals:**
- Implement a new `/subjects/search` endpoint that filters by name and/or overdue task status
- Enable Python-based logic to calculate overdue task status (due date < current time)
- Support flexible filtering: by name only, by overdue status only, or both combined with OR logic
- Return enriched subject data including overdue task count information
- Maintain backward compatibility with existing `/subjects` endpoint

**Non-Goals:**
- Creating or modifying the tasks table structure (assumed to exist or be created in a separate change)
- Building UI components for the search functionality
- Implementing full task CRUD operations (task creation/update/delete)
- Authentication changes or role-based access control modifications
- Database migrations for existing subject data

## Decisions

### 1. Search Endpoint Architecture
**Decision:** Create a new dedicated `/subjects/search` endpoint (GET) separate from the existing `/subjects` listing endpoint.

**Rationale:** 
- Separation of concerns: search is semantically different from simple listing
- Allows for more flexible filtering logic without impacting the stable listing endpoint
- Easier to add additional search filters in the future without breaking changes

**Alternatives Considered:**
- Add search parameters to existing GET `/subjects`: Would require modifying stable endpoint logic
- Create as a POST endpoint with body filters: Unnecessary complexity for read-only search

### 2. Python Integration Point
**Decision:** Implement task status calculation as a Python utility function called from XanoScript API logic, or as an addon/helper function within XanoScript.

**Rationale:**
- Python can elegantly handle date comparisons and status calculations
- Keeps business logic separate from XanoScript query logic
- Python code is testable and reusable across multiple API endpoints if needed
- Xano supports Python execution within queries or as functions

**Alternatives Considered:**
- Pure XanoScript implementation: Less readable for complex date logic, harder to test
- External Python microservice: Adds infrastructure complexity and latency

### 3. Overdue Task Detection Logic
**Decision:** Overdue tasks are those with `due_date < now()`. Uses UTC timestamps for consistency.

**Rationale:**
- Simple, deterministic logic: no ambiguity about whether a task is overdue
- UTC avoids timezone complications in a multi-region system
- Matches industry-standard task management patterns

### 4. Filter Combination Logic
**Decision:** Use OR logic for combining filters: return subjects matching (name contains X) OR (has overdue tasks).

**Rationale:**
- User request specified OR logic
- Aligns with search UX expectation: user wants subjects matching ANY of their criteria
- Simpler mental model than AND logic

### 5. Data Enrichment
**Decision:** Include `overdue_task_count` in search results to give users visibility into severity.

**Rationale:**
- Enables UI to surface most critical subjects first
- Helps prioritization without requiring additional API calls
- Minimal performance impact if calculated efficiently

## Risks / Trade-offs

**[Risk] Task Table May Not Exist Yet**
→ *Mitigation*: Design assumes tasks table will be created separately. If it doesn't exist during implementation, this endpoint gracefully returns results based on name filtering only, or the tasks table creation is prioritized as a prerequisite.

**[Risk] Scalability with Large Task Counts**
→ *Mitigation*: Ensure proper indexing on tasks table (user_id, due_date). Consider pagination of results if subject count is high.

**[Risk] Python Complexity vs. XanoScript Purist Approach**
→ *Mitigation*: Keep Python logic minimal and focused; document the Python function clearly. If performance issues arise, logic can be migrated to pure XanoScript or database-level calculations.

**[Risk] Real-time Accuracy of "Overdue" Status**
→ *Mitigation*: Overdue status is calculated at query time, so it's always current. No stale caches or background job delays.

**[Trade-off] Two Similar Endpoints (GET /subjects vs GET /subjects/search)**
→ *Justification*: Slight API fragmentation accepted for clarity and forward compatibility. Both serve different use cases.

