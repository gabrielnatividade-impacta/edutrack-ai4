# activity-grades Specification

## Purpose

Define the system's capability to allow teachers to record grades for students in specific academic activities. This specification outlines the requirements for creating, validating, and storing activity grades with proper authorization controls.

## ADDED Requirements

### Requirement: Teacher can submit a grade for a student's activity

The system SHALL allow authenticated teachers to submit a numerical grade for a student's completed activity. Grades MUST be recorded with teacher identification, timestamp, and linked to both the activity and student.

#### Scenario: Teacher successfully submits a grade
- **WHEN** an authenticated teacher submits a valid grade (0-10) for a student in an activity within their subject
- **THEN** the grade is recorded in the database with `teacher_id`, `created_at` timestamp, and returns HTTP 201 with the created grade object

#### Scenario: Teacher attempts to submit a grade outside their subject
- **WHEN** a teacher tries to submit a grade for an activity in a subject they don't teach
- **THEN** the system returns HTTP 403 Forbidden with message "You do not have permission to grade this activity"

#### Scenario: Student attempts to submit a grade
- **WHEN** an authenticated student (non-teacher) attempts to submit a grade
- **THEN** the system returns HTTP 403 Forbidden with message "Only teachers can submit grades"

#### Scenario: Invalid grade value submitted
- **WHEN** a teacher submits a grade outside the valid range (not between 0-10)
- **THEN** the system returns HTTP 400 Bad Request with message "Grade must be between 0 and 10"

#### Scenario: Non-existent student or activity referenced
- **WHEN** a teacher submits a grade for a non-existent student or activity
- **THEN** the system returns HTTP 404 Not Found with message "Student or activity not found"

### Requirement: Grade submission includes validation and error handling

The system SHALL validate all inputs before recording a grade and provide clear error messages for invalid submissions.

#### Scenario: Missing required fields
- **WHEN** a teacher submits a grade request missing required fields (`student_id`, `activity_id`, `grade`)
- **THEN** the system returns HTTP 400 Bad Request listing which fields are required

#### Scenario: Duplicate grade prevention
- **WHEN** a teacher attempts to submit a grade for the same student and activity combination that already has a recorded grade
- **THEN** the system returns HTTP 409 Conflict with message "A grade already exists for this student and activity. Update functionality coming soon."

### Requirement: Grade data is persisted with audit trail

The system SHALL store grades in a persistent database table with complete audit information for compliance and troubleshooting.

#### Scenario: Grade is saved with metadata
- **WHEN** a grade is successfully submitted
- **THEN** the database records: `id`, `activity_id`, `student_id`, `grade` (value), `teacher_id`, `created_at`, `updated_at`

#### Scenario: Grade retrieval includes metadata
- **WHEN** a grade is retrieved from storage
- **THEN** the response includes all stored fields including `teacher_id` and `created_at` for audit purposes
