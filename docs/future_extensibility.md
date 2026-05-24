# Future Extensibility Plan

This document outlines the plan for future extensibility of the subject management feature.

## 10.1 Subject-Level Event Logging

Subject-level event logging can be added without schema changes to the `subject` table. A new `event_log` table will be created to store event information, with a foreign key to the `subject` table. This is documented in more detail in `docs/subject_event_logging.md`.

## 10.2 Explicit Enrollment Tracking

Explicit enrollment tracking can be implemented in the future by creating a new `enrollment` table. This table would have foreign keys to both the `user` and `subject` tables, creating a many-to-many relationship. This would allow for tracking individual user enrollments in subjects, which is a common requirement for educational platforms.

## 10.3 Team Collaboration Patterns

The current account-subject relationship supports team collaboration patterns. Since subjects are owned by accounts, all members of an account can view and potentially collaborate on subjects, depending on their roles and permissions.

## 10.4 Open Questions

- **Cross-account subject sharing**: Should subjects be shareable across different accounts? This would require a more complex access control model, but it could be a valuable feature for collaboration between different organizations. This is a decision that can be deferred to the future.
