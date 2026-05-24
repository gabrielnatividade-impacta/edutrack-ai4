## ADDED Requirements

### Requirement: Subjects database exists
The system SHALL store academic subjects in a persistent `subjects` table.

#### Scenario: Create a subject record
- **WHEN** an authenticated user creates a subject with required fields
- **THEN** the system stores a record in `subjects` with `user_id`, `name`, `code`, timestamps, and returns the created subject

#### Scenario: Create a subject with optional metadata
- **WHEN** the user provides `semester` and `description`
- **THEN** the system stores those fields in the subject record

### Requirement: Subject field validation
The system SHALL validate required subject fields and enforce `code` uniqueness per user.

#### Scenario: Missing required fields
- **WHEN** the user omits `name` or `code`
- **THEN** the system returns 400 Bad Request with a validation error

#### Scenario: Duplicate subject code for same user
- **WHEN** the user attempts to create a subject with a `code` already used by one of their subjects
- **THEN** the system returns 400 Bad Request and does not create the subject
