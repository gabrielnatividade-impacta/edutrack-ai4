# academic-task-management Specification

## Purpose
TBD - created by archiving change academic-tasks-table. Update Purpose after archive.
## Requirements
### Requirement: Academic Task Data Storage
The system SHALL store academic tasks with the following attributes:
- title: Text field for the task title
- description: Text field for detailed task description
- due_date: Date field for the task deadline
- status: Text field indicating task status (pending, in_progress, completed, overdue)
- subject_id: Reference to the subjects table

#### Scenario: Task Creation
- **WHEN** a new academic task is created
- **THEN** all required fields (title, description, due_date, status, subject_id) SHALL be stored
- **AND** the subject_id SHALL reference an existing subject

#### Scenario: Status Validation
- **WHEN** a task status is set
- **THEN** the status SHALL be one of the predefined values: pending, in_progress, completed, overdue

### Requirement: Subject Relationship Integrity
The system SHALL maintain referential integrity between academic tasks and subjects.

#### Scenario: Valid Subject Reference
- **WHEN** creating or updating an academic task
- **THEN** the subject_id SHALL reference an existing subject in the subjects table

#### Scenario: Subject Deletion Cascade
- **WHEN** a subject is deleted
- **THEN** all associated academic tasks SHALL be deleted to maintain data consistency

