## Why

Students need a way to register and manage their academic obligations such as lessons, tests, and assignments, linked to specific subjects. This will help them stay organized and track their academic progress effectively.

## What Changes

- Create a new `academic_tasks` table with the following fields:
  - `title` (text): The title of the academic task
  - `description` (text): Detailed description of the task
  - `due_date` (date): The due date for the task
  - `status` (text): Current status of the task (e.g., pending, completed)
  - `subject_id` (reference): Foreign key linking to the `subjects` table

## Capabilities

### New Capabilities
- `academic-task-management`: Enable creation, management, and tracking of academic tasks linked to subjects

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- Database schema: New table `academic_tasks` with relationship to `subjects`
- Backend: New API endpoints for CRUD operations on academic tasks
- Frontend: UI components for task management (to be implemented later)