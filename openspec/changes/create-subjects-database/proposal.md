## Why

Academic users need a way to organize and manage the disciplinary subjects they are taking or teaching. Currently, the system lacks the ability to track which subjects belong to which users, making it impossible to implement subject-specific features, access controls, and automations that are essential for an educational platform.

## What Changes

- **New table**: `subject` - stores subject/discipline information with metadata
- **New relationship**: Users can register and manage multiple subjects (one-to-many relationship via account)
- **New capabilities**: Subject-level access control and future automations based on subject enrollment
- **Properties**: Each subject will include standard academic properties (name, code, description, credits, etc.) plus custom fields for future extensibility

## Capabilities

### New Capabilities

- `subject-management`: Create, read, update, and delete subjects. Users can register subjects associated with their account and manage subject details including name, code, description, and credits.
- `subject-access-control`: Role-based permissions for viewing, editing, and managing subjects. Different access levels for subject owners, team members, and guests.
- `subject-enrollment`: Track which users are enrolled in or managing specific subjects, supporting both individual and team-based subject management.

### Modified Capabilities

- `account-management`: Extend account to support subject associations. Accounts will now have a list of associated subjects for organizational purposes.

## Impact

- **Database**: New `subject` table with foreign key to `account` table
- **APIs**: New endpoints needed for subject CRUD operations (will be defined in specs)
- **Access Control**: Integration with existing role-based access control system for subject-level permissions
- **Frontend**: Eventual UI for subject management (part of future feature rollout)
- **Dependencies**: Relies on existing `account` and `user` tables; compatible with current authentication system
