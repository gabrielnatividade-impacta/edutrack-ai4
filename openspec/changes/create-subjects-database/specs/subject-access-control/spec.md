## ADDED Requirements

### Requirement: Subject-Level Access Control Foundation
The system SHALL enforce role-based access control at the subject level. Access permissions SHALL be determined by user's role within the account that owns the subject.

#### Scenario: Owner has full subject access
- **WHEN** account owner (role=owner) attempts to access subject owned by their account
- **THEN** system grants full permissions: create, read, update, delete, manage

#### Scenario: Admin has full subject access
- **WHEN** account admin (role=admin) attempts to access subject owned by their account
- **THEN** system grants full permissions: create, read, update, delete, manage

#### Scenario: Member has limited subject access
- **WHEN** account member (role=member) attempts to access subject owned by their account
- **THEN** system grants read and partial write permissions (view details, potentially edit subject details if allowed by future policies)

#### Scenario: Guest has read-only access
- **WHEN** account guest (role=guest) attempts to access subject owned by their account
- **THEN** system grants read-only permissions (view details only, no modifications)

### Requirement: Cross-Account Access Prevention
The system SHALL prevent users from accessing subjects that belong to accounts they are not members of. Access control checks MUST occur before any subject data is returned.

#### Scenario: User cannot access subject from different account
- **WHEN** user requests subject owned by a different account they don't belong to
- **THEN** system returns access denied error (403 Forbidden or not found)

#### Scenario: User must be account member
- **WHEN** determining subject access
- **THEN** system verifies user is member of subject's account before granting access

### Requirement: Subject Access Integration with Existing RBAC
The system SHALL integrate with the existing role_based_access_control function to determine subject permissions. Subject access checks SHALL use the same role-based patterns as account and team member management.

#### Scenario: Subject access uses account roles
- **WHEN** checking subject access
- **THEN** system uses user's existing account role (owner, admin, member, guest) to determine permissions

#### Scenario: No additional subject-specific roles initially
- **WHEN** implementing subject access control
- **THEN** system uses account-level roles without creating subject-specific role assignments (future capability)

### Requirement: Subject Visibility Rules
The system SHALL enforce rules about which subjects are visible to which users. Visibility determines whether a subject appears in lists and searches.

#### Scenario: Active subjects visible to account members
- **WHEN** user queries for subjects in their account
- **THEN** system returns all active subjects (is_active=true) for that account based on user's role

#### Scenario: Inactive subjects visible only to admins and owner
- **WHEN** user queries for inactive subjects
- **THEN** system returns inactive subjects only if user has admin or owner role

#### Scenario: Subjects from other accounts are never visible
- **WHEN** user queries subjects
- **THEN** system filters results to only include subjects from accounts user is member of

### Requirement: Future Subject-Level Automation
The system SHALL be designed to support future subject-specific automations. Access control structure MUST allow for extension to subject-level triggers and automations.

#### Scenario: Subject access control structure supports future extensions
- **WHEN** designing subject access control
- **THEN** system architecture allows for future subject-level event logging, audit trails, and role refinement without major refactoring
