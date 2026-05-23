## Context

This design document outlines the technical approach for implementing the `academic_tasks` table within the EduTrack AI project. The goal is to provide students with the ability to record and manage their academic obligations, such as lessons, exams, and assignments, linking them to specific subjects. This feature aims to enhance student organization and tracking of their academic workload.

## Goals / Non-Goals

**Goals:**
- To create a new database table named `academic_tasks` with a clearly defined schema.
- To establish a one-to-many relationship between the `subjects` table and the `academic_tasks` table, allowing each task to be associated with a single subject.
- To store essential information for each academic task, including its title, description, due date, status, and the associated subject.

**Non-Goals:**
- This design does not include the creation of API endpoints for CRUD (Create, Read, Update, Delete) operations on the `academic_tasks` table. These will be addressed in a subsequent implementation phase.
- This design does not cover any frontend UI development for displaying or managing academic tasks.

## Decisions

**Data Model for `academic_tasks` table:**
- `id`: (int) Primary key, auto-incrementing.
- `created_at`: (timestamp) Timestamp of record creation.
- `updated_at`: (timestamp) Timestamp of last update.
- `title`: (text) The name or title of the academic task (e.g., "Algebra Homework 1", "Midterm Exam").
- `description`: (text) A detailed description of the task.
- `due_date`: (date) The deadline for the academic task.
- `status`: (text) The current status of the task (e.g., "pending", "completed", "in_progress", "overdue"). Default to "pending".
- `subject_id`: (int) Foreign key referencing the `id` field of the `subject` table. This links the task to a specific academic subject.
- `is_active`: (bool) Flag for soft deletion, defaults to true.

**Relationship with `subject` table:**
- `academic_tasks` will have a `subject_id` field that references the `id` in the `subject` table, establishing a one-to-many relationship.

## Risks / Trade-offs

- **Risk**: Data inconsistency if an `academic_task` references a `subject_id` that no longer exists.
- **Mitigation**: Rely on XanoScript's implicit foreign key handling for `table` references, which typically enforces referential integrity. Further application-level validation can be added during API development.

## Open Questions

- What is the definitive set of allowed values for the `status` field? (e.g., "pending", "completed", "in_progress", "overdue"). For initial implementation, a free-form text field will be used, with the understanding that this might be formalized into an enum or lookup table later.