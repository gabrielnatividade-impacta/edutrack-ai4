## ADDED Requirements

### Requirement: Account Subject Association
The system SHALL extend the account management to support association with subjects. Accounts are the organizational unit that owns and manages subjects.

#### Scenario: Account can have multiple subjects
- **WHEN** creating subjects
- **THEN** multiple subjects can be associated with the same account through account_id foreign key

#### Scenario: Subject ownership is account-level
- **WHEN** managing subjects
- **THEN** subjects are owned by the account as an entity, not individual users, enabling team collaboration

#### Scenario: Account subject list
- **WHEN** account details are retrieved
- **THEN** account data structure supports including associated subjects (implementation detail for API design)

### Requirement: Subject Management as Account Feature
The system SHALL present subject management as a feature of account management. Account admins and owners can manage all subjects owned by their account.

#### Scenario: Account admin manages account subjects
- **WHEN** account admin accesses account management interface/API
- **THEN** admin can view, create, edit, and manage all subjects owned by the account

#### Scenario: Account owner manages account subjects
- **WHEN** account owner accesses account management
- **THEN** owner has full control over account subjects including creation, modification, and deletion

#### Scenario: Subject context in account operations
- **WHEN** performing account operations
- **THEN** system maintains subject association throughout account lifecycle (e.g., when account is archived, subjects should be handled appropriately)

### Requirement: Account Deletion with Subject Cascade
The system SHALL ensure that when an account is deleted, all associated subjects are properly handled. Cascade delete behavior MUST be enforced.

#### Scenario: Account deletion removes all subjects
- **WHEN** account is deleted
- **THEN** all subjects owned by that account are automatically deleted (cascade delete)

#### Scenario: Subject cleanup is atomic with account deletion
- **WHEN** deleting account
- **THEN** account and all subjects are deleted as single atomic operation, preventing orphaned subjects

### Requirement: Subject Support in Account Lifecycle
The system SHALL support subjects throughout account lifecycle operations (creation, modification, deletion, archival).

#### Scenario: New accounts can have subjects
- **WHEN** creating new account
- **THEN** account is ready to accept subject creation immediately upon creation

#### Scenario: Account modification doesn't affect subjects
- **WHEN** modifying account properties (name, description, etc.)
- **THEN** subject associations and data remain unaffected

#### Scenario: Account archival considers subjects
- **WHEN** account is archived (if archival feature exists)
- **THEN** subjects should either be archived with account or handled according to business rules (deferred decision)
