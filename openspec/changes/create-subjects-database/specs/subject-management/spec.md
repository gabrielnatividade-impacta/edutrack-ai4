## ADDED Requirements

### Requirement: Subject Database Table
The system SHALL provide a database table to store subject/discipline information with standardized academic properties. Each subject entry SHALL include identification, descriptive, and academic metadata.

#### Scenario: Subject table exists with core fields
- **WHEN** querying the database schema
- **THEN** the `subject` table exists with fields: id (unique identifier), account_id (foreign key), name, code, description, credits, semester, year, color (optional), tags (optional), is_active, created_at, updated_at

#### Scenario: Subject is associated with account
- **WHEN** creating a subject record
- **THEN** the subject MUST be associated with exactly one account via account_id foreign key

#### Scenario: Subject cannot exist without account
- **WHEN** attempting to delete an account
- **THEN** all associated subjects are automatically removed (cascade delete)

### Requirement: Subject Creation
The system SHALL allow authorized users to create new subjects associated with their account. A created subject MUST include all required properties.

#### Scenario: Subject created with minimum required fields
- **WHEN** authorized user submits subject creation request with name, code, and account_id
- **THEN** system creates subject record with generated id, timestamps, and default values (is_active=true, credits=null, semester=null, year=null)

#### Scenario: Subject created with complete academic information
- **WHEN** authorized user submits subject creation with all fields (name, code, description, credits, semester, year, color, tags)
- **THEN** system stores all provided data and returns complete subject record

### Requirement: Subject Retrieval
The system SHALL provide methods to retrieve subject data by various filters. Subject queries MUST support account-scoped filtering for access control.

#### Scenario: Retrieve single subject by id
- **WHEN** user requests subject by id with valid account context
- **THEN** system returns subject record if it belongs to user's account, or returns error if access denied

#### Scenario: List all subjects for an account
- **WHEN** user requests subjects list filtered by account_id
- **THEN** system returns array of active subjects for that account, supporting pagination

#### Scenario: List all subjects including inactive
- **WHEN** user requests subjects with is_active filter set to false or null
- **THEN** system returns matching subjects regardless of active status

### Requirement: Subject Update
The system SHALL allow authorized users to modify subject properties. Updates MUST preserve data integrity and track changes.

#### Scenario: Update subject basic information
- **WHEN** authorized user submits update request with new name, code, or description
- **THEN** system updates subject record and reflects changes in updated_at timestamp

#### Scenario: Update academic properties
- **WHEN** user updates credits, semester, or year fields
- **THEN** system accepts numeric/valid values and updates record accordingly

#### Scenario: Activate or deactivate subject
- **WHEN** authorized user sets is_active flag to true or false
- **THEN** system updates subject status without deleting record, preserving historical data

### Requirement: Subject Deletion
The system SHALL support both soft and hard deletion of subjects. Soft deletion (deactivation) preserves data; hard deletion removes record.

#### Scenario: Soft delete via deactivation
- **WHEN** user deactivates a subject (is_active=false)
- **THEN** subject is marked inactive but remains in database for historical tracking

#### Scenario: Hard delete removes subject
- **WHEN** authorized user requests hard deletion of subject
- **THEN** subject record is permanently removed from database (if such endpoint is provided)

### Requirement: Subject Properties Structure
The system SHALL store subject data with the following field specifications:

#### Scenario: Field validation and types
- **WHEN** creating or updating a subject
- **THEN** system validates: name (required, string, max 255), code (required, string, unique per account, max 50), description (optional, string, max 1000), credits (optional, numeric), semester (optional, string), year (optional, numeric), color (optional, string hex format), tags (optional, array/list), is_active (boolean, default true), created_at (timestamp), updated_at (timestamp)

#### Scenario: Code uniqueness within account
- **WHEN** attempting to create subject with code that already exists for same account
- **THEN** system rejects creation with uniqueness violation error

### Requirement: Subject Relationship to Account
The system SHALL enforce that subjects are owned by accounts and cannot be orphaned. The relationship MUST be enforced at database level.

#### Scenario: Foreign key integrity
- **WHEN** querying subject records
- **THEN** every subject record has valid account_id that references existing account

#### Scenario: Account deletion cascades to subjects
- **WHEN** an account is deleted
- **THEN** all associated subject records are automatically deleted (cascade behavior)
