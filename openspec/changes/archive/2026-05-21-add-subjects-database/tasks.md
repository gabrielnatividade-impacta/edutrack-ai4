## 1. Database Setup

- [x] 1.1 Create `subjects` table in Xano with schema (id, user_id, name, code, semester, description, created_at, updated_at)
- [x] 1.2 Add foreign key relationship from subject.user_id to user.id
- [x] 1.3 Add indexes on user_id for fast user subject lookups
- [x] 1.4 Add unique constraint on (user_id, code) to prevent duplicate subject codes per user

## 2. API Endpoints - Read Operations

- [x] 2.1 Create GET `/subjects` endpoint to list all subjects for authenticated user
- [x] 2.2 Create GET `/subjects/{id}` endpoint to retrieve single subject with ownership validation
- [x] 2.3 Implement pagination/filtering for subject list endpoint (optional parameters: limit, offset, semester)

## 3. API Endpoints - Write Operations

- [x] 3.1 Create POST `/subjects` endpoint to create new subject with validation (name, code required)
- [x] 3.2 Create PUT `/subjects/{id}` endpoint to update subject with ownership check
- [x] 3.3 Create DELETE `/subjects/{id}` endpoint to delete subject with ownership verification

## 4. Access Control & Authorization

- [x] 4.1 Implement authentication check on all subject endpoints (401 if no valid token)
- [x] 4.2 Implement ownership verification in GET single subject operation
- [x] 4.3 Implement ownership verification in PUT update operation
- [x] 4.4 Implement ownership verification in DELETE operation
- [x] 4.5 Ensure all unauthorized access attempts return 404 (not 403) to hide resource existence
- [x] 4.6 Make user_id immutable - prevent attempts to change subject owner via PUT

## 5. Data Validation & Response Formatting

- [x] 5.1 Validate required fields (name, code) on create/update operations
- [x] 5.2 Validate field lengths and formats (e.g., code max 20 chars)
- [x] 5.3 Return proper HTTP status codes (201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 204 No Content)
- [x] 5.4 Ensure all responses use RFC3339 datetime format for timestamps
- [x] 5.5 Return complete subject object in responses (all fields including user_id, timestamps)

## 6. Event Logging Integration

- [x] 6.1 Log "subject_created" event when subject is created (user_id, subject_id, timestamp)
- [x] 6.2 Log "subject_updated" event when subject is modified (user_id, subject_id, changed_fields)
- [x] 6.3 Log "subject_deleted" event when subject is deleted (user_id, subject_id, timestamp)
- [x] 6.4 Log "subject_access_denied" event when unauthorized access attempt occurs
- [x] 6.5 Implement async logging (fire-and-forget) to avoid blocking subject operations

## 7. Testing & Validation

- [x] 7.1 Test subject creation with valid data
- [x] 7.2 Test subject creation with missing required fields
- [x] 7.3 Test subject list retrieval for authenticated user
- [x] 7.4 Test subject retrieval by ID with ownership validation
- [x] 7.5 Test subject update for owned subject
- [x] 7.6 Test update attempts on subjects owned by other users (should return 404)
- [x] 7.7 Test subject deletion for owned subject
- [x] 7.8 Test deletion attempts on subjects owned by other users (should return 404)
- [x] 7.9 Test unauthenticated access attempts (should return 401)
- [x] 7.10 Test that user_id cannot be changed via PUT request
- [x] 7.11 Test event logging for all operations
- [x] 7.12 Test edge cases (empty strings, null values, very long strings)

## 8. Documentation & Deployment

- [x] 8.1 Document API endpoints in Xano API documentation (method, path, auth, params, responses)
- [x] 8.2 Create example requests/responses for subject CRUD operations
- [x] 8.3 Document error codes and their meanings (400, 401, 404, etc.)
- [ ] 8.4 Verify database schema and API endpoints are synced with Xano backend
- [ ] 8.5 Perform manual smoke testing with real API calls
