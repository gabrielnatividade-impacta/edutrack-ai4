## ADDED Requirements

### Requirement: User can create a subject
The system SHALL allow authenticated users to create a new academic subject with required metadata. The created subject SHALL be associated with the authenticated user as owner.

#### Scenario: Successful subject creation
- **WHEN** an authenticated user sends POST request to `/subjects` with required fields (name, code)
- **THEN** system creates subject record with unique ID, associates it to user, sets timestamps, and returns 201 with created subject data

#### Scenario: Subject creation with optional fields
- **WHEN** user provides optional fields (semester, description)
- **THEN** system stores these fields in the subject record

#### Scenario: Subject creation with missing required fields
- **WHEN** user omits required fields (name or code)
- **THEN** system returns 400 Bad Request with validation error message

### Requirement: User can retrieve their subjects
The system SHALL allow authenticated users to fetch a list of all subjects they own.

#### Scenario: Retrieve empty subject list
- **WHEN** newly registered user requests GET `/subjects`
- **THEN** system returns 200 with empty array

#### Scenario: Retrieve populated subject list
- **WHEN** user with 3 subjects requests GET `/subjects`
- **THEN** system returns 200 with array containing exactly 3 subject objects with all fields populated

#### Scenario: Retrieve single subject by ID
- **WHEN** user requests GET `/subjects/{id}` for a subject they own
- **THEN** system returns 200 with complete subject data

### Requirement: User can update their subject
The system SHALL allow authenticated users to modify subject fields they own.

#### Scenario: Update subject name
- **WHEN** user sends PUT `/subjects/{id}` with new name value
- **THEN** system updates name, sets updated_at timestamp, and returns 200 with modified subject

#### Scenario: Update multiple subject fields
- **WHEN** user sends PUT `/subjects/{id}` with new name, code, and semester
- **THEN** system updates all provided fields and returns complete updated subject

#### Scenario: Partial update preserves unchanged fields
- **WHEN** user updates only subject description while leaving name unchanged
- **THEN** name remains original value, description updates, other fields unchanged

### Requirement: User can delete their subject
The system SHALL allow authenticated users to permanently delete subjects they own.

#### Scenario: Successful subject deletion
- **WHEN** user sends DELETE `/subjects/{id}` for subject they own
- **THEN** system removes subject record and returns 204 No Content

#### Scenario: Deletion removes all subject data
- **WHEN** user deletes subject and immediately tries to GET it
- **THEN** system returns 404 Not Found

### Requirement: Subject has consistent data structure
The system SHALL maintain subject records with a consistent schema for all CRUD operations.

#### Scenario: Created subject has all required fields
- **WHEN** subject is created
- **THEN** response includes id, user_id, name, code, created_at, updated_at fields

#### Scenario: Optional fields included when provided
- **WHEN** subject created with semester and description
- **THEN** response includes semester and description fields with provided values

#### Scenario: Timestamps are RFC3339 formatted
- **WHEN** subject created or updated
- **THEN** created_at and updated_at values are valid RFC3339 datetime strings
