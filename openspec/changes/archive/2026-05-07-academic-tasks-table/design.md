## Context

This design implements the academic_tasks table as proposed, building on the existing subjects table in the Xano backend. The subjects table already exists and manages academic subjects/disciplines. The academic_tasks table will extend this by allowing students to track specific obligations (lessons, tests, assignments) tied to each subject.

## Goals / Non-Goals

**Goals:**
- Create a robust database schema for academic tasks with proper relationships
- Ensure data integrity through foreign key constraints
- Support common task statuses and due date tracking
- Follow XanoScript best practices for table design

**Non-Goals:**
- Implement API endpoints (covered in separate tasks)
- Create frontend UI components
- Add advanced features like task notifications or recurring tasks

## Decisions

- **Primary Key**: Use `id` (int/uuid) as primary key, following Xano conventions
- **Foreign Key**: `subject_id` references `subjects.id` with cascade delete to maintain referential integrity
- **Status Field**: Use text field with predefined values (pending, in_progress, completed, overdue) for flexibility
- **Date Field**: Use date type for `due_date` to support date-based queries and validation
- **Text Fields**: Use text type for `title` and `description` to accommodate varying lengths
- **Table Creation Order**: Create academic_tasks table after confirming subjects table exists, then add the foreign key relationship

## Risks / Trade-offs

- **Data Consistency**: Foreign key ensures tasks are linked to valid subjects, but requires subjects to exist first
- **Status Flexibility**: Text field allows custom statuses but may require validation in application logic
- **Performance**: Date field enables efficient queries but may need indexing for large datasets