# API CRUD - Subjects

## Overview
Endpoints to manage `subjects` for authenticated users. All endpoints require a valid auth token and enforce ownership: users may only access and modify their own subjects.

Base path: `/subjects`

Authentication: Bearer token (JWT or Xano session)

Fields (subject):
- `id` (int, primary key)
- `user_id` (int, owner) — set server-side
- `name` (string, required)
- `code` (string, required, max 20)
- `semester` (string, optional)
- `description` (string, optional)
- `created_at` (string, RFC3339)
- `updated_at` (string, RFC3339)

---

## GET /subjects
List subjects owned by the authenticated user.

Query params:
- `limit` (int, optional)
- `offset` (int, optional)
- `semester` (string, optional)

Response 200:
{
  "items": [
    {
      "id": 123,
      "user_id": 45,
      "name": "Biology",
      "code": "BIO101",
      "semester": "Fall",
      "description": "Introductory biology",
      "created_at": "2026-05-20T12:00:00Z",
      "updated_at": "2026-05-20T12:00:00Z"
    }
  ],
  "count": 1,
  "limit": 50,
  "offset": 0
}

Errors:
- 401 Unauthorized — missing/invalid token

Notes:
- Only return subjects where `subject.user_id == current_user.id`.
- Support pagination with `limit`/`offset` defaults.

---

## GET /subjects/{id}
Retrieve a single subject by id. Must be owned by the authenticated user.

Response 200:
{
  "id": 123,
  "user_id": 45,
  "name": "Biology",
  "code": "BIO101",
  "semester": "Fall",
  "description": "Introductory biology",
  "created_at": "2026-05-20T12:00:00Z",
  "updated_at": "2026-05-20T12:00:00Z"
}

Errors:
- 401 Unauthorized
- 404 Not Found — subject not found or not owned by user (do not reveal existence)

Notes:
- Perform ownership check; return 404 when `user_id` differs.

---

## POST /subjects
Create a new subject. `user_id` is assigned from authenticated user and cannot be set by the client.

Request body:
{
  "name": "string",
  "code": "string",
  "semester": "string",        // optional
  "description": "string"    // optional
}

Response 201: {subject}

Errors:
- 400 Bad Request — validation errors (missing `name`/`code`, invalid lengths)
- 401 Unauthorized

Notes:
- Validate `code` max length 20 and required fields.
- After successful creation, log event `subject_created` with `{ user_id, subject_id }`.
- Use asynchronous logging: queue subject event metadata and process it in a background task, so subject creation remains fast.

---

## PATCH /subjects/{id}
Update an existing subject owned by the authenticated user.

Request body (any subset):
{
  "name": "string",
  "code": "string",
  "semester": "string",
  "description": "string"
}

Response 200:
{
  "id": 124,
  "user_id": 45,
  "name": "Advanced Chemistry",
  "code": "CHEM101",
  "semester": "Summer",
  "description": "Basic chemistry",
  "created_at": "2026-05-20T12:05:00Z",
  "updated_at": "2026-05-20T12:10:00Z"
}

Errors:
- 400 Bad Request — validation errors
- 401 Unauthorized
- 404 Not Found — not found or not owned by user

Notes:
- Reject attempts to change `user_id` if present in payload.
- On success, log `subject_updated` with `{ user_id, subject_id, changed_fields }`.
- The response must still include `user_id` and timestamps.

---

## DELETE /subjects/{id}
Delete a subject owned by the authenticated user.

Response 204 No Content

Errors:
- 401 Unauthorized
- 404 Not Found — not found or not owned by user

Notes:
- On success, log `subject_deleted` with `{ user_id, subject_id }`.
- Delete should also queue the event asynchronously and return immediately.

---

## Error Codes
- `400 Bad Request` — request validation failed, such as missing required fields or invalid field lengths
- `401 Unauthorized` — invalid or missing authentication token
- `404 Not Found` — subject not found or not accessible to the current user

## Example Request/Response Summary
### Create subject
POST `/subjects`
Request body:
```json
{
  "name": "Physics",
  "code": "PHY101",
  "semester": "Fall",
  "description": "Introductory physics"
}
```
Response 201: created subject JSON

### Update subject
PUT `/subjects/{id}`
Request body:
```json
{
  "name": "Physics II"
}
```
Response 200: updated subject JSON

### Delete subject
DELETE `/subjects/{id}`
Response 204 No Content
- Unauthorized access to a subject should also enqueue a `subject_access_denied` event for audit and monitoring.

---

## Common Validation Rules
- `name` and `code` are required on create; `code` max 20 chars.
- `user_id` must always be assigned server-side; ignore or error if provided in request.
- Use RFC3339 for `created_at`/`updated_at`.

## Testing Scenarios (high level)
- Create subject with valid data (201)
- Create subject with missing required fields (400)
- List subjects returns only current user's subjects
- Retrieve subject owned by user (200)
- Retrieve subject not owned by user (404)
- Update subject owned by user (200) and verify changes
- Update subject with `user_id` in payload (400 or ignore)
- Delete subject owned by user (204)
- Unauthorized access attempts (401)

