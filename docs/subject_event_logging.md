# Subject Event Logging Plan

This document outlines the plan for integrating event logging with subject CRUD operations.

## 7.1 Event Logging Structure

The following events will be logged for subject operations:

- `subject.created`: When a new subject is created.
- `subject.updated`: When a subject's details are updated.
- `subject.deleted`: When a subject is deleted.

Each event log entry will contain the following information:
- `event_name`: The name of the event (e.g., `subject.created`).
- `account_id`: The ID of the account that owns the subject.
- `user_id`: The ID of the user who performed the action.
- `subject_id`: The ID of the subject that was affected.
- `changes`: A JSON object containing the changes that were made (for `subject.updated` events).
- `created_at`: The timestamp of the event.

## 7.2 Integration with Subject CRUD Operations

The `create_event_log` function will be called from the subject API endpoints to log these events.

- **POST /api/members_accounts/subjects**: After a subject is successfully created, a `subject.created` event will be logged.
- **PATCH /api/members_accounts/subjects/{id}**: After a subject is successfully updated, a `subject.updated` event will be logged. The `changes` payload will contain the old and new values of the updated fields.
- **DELETE /api/members_accounts/subjects/{id}**: After a subject is successfully deleted, a `subject.deleted` event will be logged.

## 7.3 Extensibility

The `subject` table schema is already extensible. The `event_log` table will store the event information, and it will have a foreign key to the `subject` table. This design does not require any changes to the `subject` table.
