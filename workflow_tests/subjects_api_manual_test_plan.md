# Subjects API Manual Test Plan

## Purpose
Validate the `subjects` CRUD workflow and ownership-based access control for authenticated users.

## Setup
1. Create two test users with valid authentication tokens: `user_a` and `user_b`.
2. Use the existing authentication APIs to obtain tokens for each user.
3. Ensure the `subjects` table is available and empty or seeded cleanly.

## Test Cases

### 1. Create subject with valid data
- Request: POST `/subjects`
- Auth: `user_a`
- Body:
  - `name`: "Algebra"
  - `code`: "ALG101"
  - `semester`: "2026-1"
  - `description`: "Fundamentals of algebra"
- Expected:
  - HTTP 201 Created
  - Response contains `user_id` equal to `user_a` ID
  - Response contains `id`, `name`, `code`, `semester`, `description`, `created_at`, `updated_at`

### 2. Create subject with missing required fields
- Request: POST `/subjects`
- Auth: `user_a`
- Body: omit `name` or `code`
- Expected:
  - HTTP 400 Bad Request
  - Validation error message for missing required fields

### 3. Create subject with duplicate code for same user
- Request: POST `/subjects`
- Auth: `user_a`
- Body using `code` already created for `user_a`
- Expected:
  - HTTP 400 Bad Request
  - Error message about duplicate subject code

### 4. List subjects for authenticated user
- Request: GET `/subjects?limit=50&offset=0`
- Auth: `user_a`
- Expected:
  - HTTP 200 OK
  - Response list contains only subjects owned by `user_a`

### 5. Retrieve a subject by ID with ownership validation
- Request: GET `/subjects/{id}`
- Auth: `user_a`
- Expected:
  - HTTP 200 OK
  - Response contains the subject details

### 6. Retrieve a subject that belongs to another user
- Request: GET `/subjects/{id}` where the subject belongs to `user_b`
- Auth: `user_a`
- Expected:
  - HTTP 404 Not Found
  - Event log `subject_access_denied` should be created

### 7. Update an owned subject
- Request: PUT `/subjects/{id}`
- Auth: `user_a`
- Body:
  - `name`: "Advanced Algebra"
  - `semester`: "2026-2"
- Expected:
  - HTTP 200 OK
  - Response contains updated `name`, `semester`, and updated timestamp
  - Event log `subject_updated` should be created

### 8. Update a subject owned by another user
- Request: PUT `/subjects/{id}` for `user_b` subject
- Auth: `user_a`
- Expected:
  - HTTP 404 Not Found
  - Event log `subject_access_denied` should be created

### 9. Delete an owned subject
- Request: DELETE `/subjects/{id}`
- Auth: `user_a`
- Expected:
  - HTTP 204 No Content
  - Subject is no longer retrievable
  - Event log `subject_deleted` should be created

### 10. Delete a subject owned by another user
- Request: DELETE `/subjects/{id}` for `user_b` subject
- Auth: `user_a`
- Expected:
  - HTTP 404 Not Found
  - Event log `subject_access_denied` should be created

### 11. Unauthenticated access attempts
- Request: any `/subjects` endpoint without auth token
- Expected:
  - HTTP 401 Unauthorized

### 12. Immutability of `user_id`
- Request: PUT `/subjects/{id}` with `user_id` in the payload
- Auth: `user_a`
- Expected:
  - Subject owner remains unchanged
  - Request does not allow ownership transfer

### 13. Edge cases
- Create or update with empty strings for optional fields
- Create with maximum length `code` values
- Update with `code` already used by another subject owned by same user

## Notes
- Confirm logs in `event_log` for `subject_created`, `subject_updated`, `subject_deleted`, and `subject_access_denied`.
- Verify timestamps use RFC3339 formatting.
