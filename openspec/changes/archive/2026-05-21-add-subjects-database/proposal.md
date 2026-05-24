## Why

Students need a way to organize and track their academic subjects/disciplines within EduTrack. Currently, there's no mechanism for users to register, manage, and control access to their courses. This is a foundational capability required for future features like assignments, grades, attendance tracking, and course-specific automations.

## What Changes

- New `subjects` database table to store user courses/disciplines with ownership tracking
- API endpoints for subject CRUD operations (create, read, update, delete)
- Access control to ensure users can only manage their own subjects
- Subject data structure supporting academic metadata (code, name, semester, owner)
- Foundation for future automations tied to specific subjects

## Capabilities

### New Capabilities

- `subject-management`: Core ability for users to create, retrieve, update, and delete their academic subjects/disciplines with full ownership and CRUD operations
- `subject-access-control`: Authorization layer ensuring users can only view, modify, or delete subjects they own, with role-based controls for future admin operations

### Modified Capabilities

- `event-logging`: Subject-related operations (creation, deletion, modifications) will be logged to the event_log table for audit trails

## Impact

- **Database**: New `subjects` table with foreign key relationship to `user` table
- **APIs**: New authentication API group `/subjects/*` with endpoints for subject CRUD
- **Access Control**: All subject operations require user authentication and ownership verification
- **Event System**: Subject operations will generate event log entries for audit purposes
- **Future Systems**: Enables build of assignment, grade, and attendance tracking features tied to specific subjects
