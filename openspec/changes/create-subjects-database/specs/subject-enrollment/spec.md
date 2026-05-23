## ADDED Requirements

### Requirement: Subject and Account Association
The system SHALL establish a clear relationship between subjects and accounts. A subject belongs to exactly one account, establishing ownership and access scoping.

#### Scenario: Subject is owned by account
- **WHEN** creating a subject
- **THEN** subject is assigned to account specified in account_id field, establishing ownership

#### Scenario: Account owns multiple subjects
- **WHEN** account has multiple subjects
- **THEN** system supports one-to-many relationship where one account can own many subjects

#### Scenario: All account members can view account subjects
- **WHEN** user is member of account
- **THEN** user can view subjects owned by that account (subject to role-based visibility rules)

### Requirement: Subject-User Association Tracking
The system SHALL track which users are associated with subjects, enabling future enrollment and assignment features. User-subject relationships are established through account membership.

#### Scenario: User association via account membership
- **WHEN** user is member of account that owns subject
- **THEN** user is implicitly associated with all subjects in that account

#### Scenario: Association type determined by user role
- **WHEN** determining user's relationship with subject
- **THEN** association type (owner, admin, member, guest) is determined by user's role in the owning account

#### Scenario: Future explicit enrollment support
- **WHEN** designing subject-user relationships
- **THEN** system architecture supports future explicit enrollment relationships (e.g., user explicitly enrolled in subject) without requiring schema changes

### Requirement: Subject List Scoping by Account
The system SHALL scope subject lists to the appropriate account context. Queries for subjects MUST be filtered by account.

#### Scenario: Query subjects for specific account
- **WHEN** user requests subjects filtered by account_id
- **THEN** system returns subjects belonging to that account if user is account member

#### Scenario: User can only access subjects from their accounts
- **WHEN** user queries subjects
- **THEN** system returns subjects only from accounts user is member of

#### Scenario: Subject enrollment context
- **WHEN** user enrolls in or is assigned to subject
- **THEN** relationship is established through account membership and subject ownership

### Requirement: Subject Data Available to Team Members
The system SHALL make subject data available to all members of the account that owns the subject. Subject information MUST be accessible based on account membership status.

#### Scenario: Subject details accessible to account members
- **WHEN** account member requests subject details
- **THEN** system returns full subject information if they have appropriate access level

#### Scenario: Subject metadata includes ownership information
- **WHEN** retrieving subject
- **THEN** response includes account_id and timestamps to establish ownership context

### Requirement: Enrollment Extensibility
The system SHALL be designed to support future enrollment tracking without structural changes. Initial implementation establishes foundations for more complex enrollment features.

#### Scenario: Account-based association is foundation
- **WHEN** designing subject access
- **THEN** account ownership is the base layer; future explicit enrollment (user enrolled in course X) can be built on top

#### Scenario: Future enrollment table compatibility
- **WHEN** planning architecture
- **THEN** subject table structure and account relationship are compatible with future enrollment tracking table that links users explicitly to subjects
