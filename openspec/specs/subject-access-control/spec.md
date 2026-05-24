# subject-access-control Specification

## Purpose
TBD - created by archiving change add-subjects-database. Update Purpose after archive.
## Requirements
### Requirement: Subject endpoints require authentication
The system SHALL require valid authentication tokens for all subject operations. Unauthenticated requests SHALL be rejected with 401 Unauthorized.

#### Scenario: Unauthenticated user cannot access subjects
- **WHEN** user sends GET `/subjects` without authentication token
- **THEN** system returns 401 Unauthorized

#### Scenario: Unauthenticated create attempt rejected
- **WHEN** user sends POST `/subjects` without authentication
- **THEN** system returns 401 Unauthorized, no subject created

#### Scenario: Invalid token rejected
- **WHEN** user sends request with malformed or expired authentication token
- **THEN** system returns 401 Unauthorized

#### Scenario: Valid token grants access
- **WHEN** authenticated user sends GET `/subjects` with valid token
- **THEN** system returns 200 with user's subjects

### Requirement: Users can only access their own subjects
The system SHALL enforce ownership-based access control. Users SHALL only retrieve, update, or delete subjects where they are the owner.

#### Scenario: User cannot retrieve another user's subject
- **WHEN** user A requests GET `/subjects/{id}` where id belongs to user B
- **THEN** system returns 404 Not Found (hiding existence from unauthorized users)

#### Scenario: User cannot update another user's subject
- **WHEN** user A sends PUT `/subjects/{id}` where id belongs to user B
- **THEN** system returns 404 Not Found, subject unchanged

#### Scenario: User cannot delete another user's subject
- **WHEN** user A sends DELETE `/subjects/{id}` where id belongs to user B
- **THEN** system returns 404 Not Found, subject not deleted

#### Scenario: User can access only their own subjects in list
- **WHEN** user A requests GET `/subjects`
- **THEN** system returns 200 with only subjects where user_id matches user A, never subjects from user B

#### Scenario: Ownership is immutable after creation
- **WHEN** user tries to change user_id of subject via PUT request
- **THEN** system ignores user_id field and preserves original owner

### Requirement: Authorization is enforced at request time
The system SHALL check ownership authorization before performing any operation on a subject.

#### Scenario: Authorization checked before update
- **WHEN** user A attempts to update subject owned by user B
- **THEN** authorization check happens first, returns 404 before any data modification

#### Scenario: Authorization checked before deletion
- **WHEN** user A attempts to delete subject owned by user B
- **THEN** authorization check happens first, returns 404, subject remains intact

### Requirement: Audit trail for access control events
The system SHALL log all successful and failed subject access attempts for security audit.

#### Scenario: Successful subject access is logged
- **WHEN** user successfully retrieves their subject
- **THEN** event logged with action "subject_accessed" and user context

#### Scenario: Unauthorized access attempt is logged
- **WHEN** user attempts unauthorized subject access
- **THEN** event logged with action "subject_access_denied" and attempt details

#### Scenario: Ownership mismatch logged
- **WHEN** user attempts access to subject they don't own
- **THEN** event logged with user_id, subject_id, and action "subject_unauthorized_attempt"

