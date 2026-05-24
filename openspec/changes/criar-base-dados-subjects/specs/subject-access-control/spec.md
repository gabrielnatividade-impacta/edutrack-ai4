## ADDED Requirements

### Requirement: Subject ownership association
The system SHALL associate each subject with the authenticated user who created it using the `user_id` field.

#### Scenario: Subject record includes owner reference
- **WHEN** a subject is created
- **THEN** the stored subject record contains `user_id` equal to the authenticated user's ID

### Requirement: Subject access control
The system SHALL allow only the subject owner to access, update, or delete that subject.

#### Scenario: Unauthorized subject access
- **WHEN** a user requests a subject that belongs to another user
- **THEN** the system returns 404 Not Found or access denied

#### Scenario: Unauthorized subject modification
- **WHEN** a user attempts to update or delete a subject they do not own
- **THEN** the system rejects the request with an access error
