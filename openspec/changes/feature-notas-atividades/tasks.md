## 1. Database

- [ ] 1.1 Create `activity_grades` table with fields: `id`, `activity_id`, `student_id`, `grade`, `teacher_id`, `created_at`, `updated_at`
- [ ] 1.2 Add foreign key relationships: `activity_id` → `academic_tasks`, `student_id` → `users`, `teacher_id` → `users`
- [ ] 1.3 Add unique constraint on `(activity_id, student_id)` to prevent duplicate grades
- [ ] 1.4 Add indexes on `activity_id` and `student_id` for query performance

## 2. API Endpoint

- [ ] 2.1 Create POST endpoint `/academic_tasks/{task_id}/grades` in the `subjects` API group
- [ ] 2.2 Implement request body validation: `student_id` (required), `grade` (required, 0-10 range)
- [ ] 2.3 Implement authentication check: require valid Xano auth session
- [ ] 2.4 Implement authorization: verify caller is a teacher and teaches the subject containing the activity

## 3. Response & Error Handling

- [ ] 3.1 Return HTTP 201 with created grade object on success (include `id`, `activity_id`, `student_id`, `grade`, `teacher_id`, `created_at`)
- [ ] 3.2 Return HTTP 403 Forbidden if user is not a teacher or doesn't teach the subject
- [ ] 3.3 Return HTTP 404 Not Found if activity or student doesn't exist
- [ ] 3.4 Return HTTP 400 Bad Request for invalid inputs (missing fields, grade out of range, invalid student/activity)
- [ ] 3.5 Return HTTP 409 Conflict if grade already exists for the same student-activity combination

## 4. Testing

- [ ] 4.1 Manual test: Teacher successfully submits a grade (verify record appears in database)
- [ ] 4.2 Manual test: Student attempts to submit a grade (verify HTTP 403 response)
- [ ] 4.3 Manual test: Teacher submits grade for activity outside their subject (verify HTTP 403 response)
- [ ] 4.4 Manual test: Invalid grade value (e.g., 15) (verify HTTP 400 response)
- [ ] 4.5 Manual test: Missing required fields (verify HTTP 400 response)
- [ ] 4.6 Manual test: Duplicate grade attempt (verify HTTP 409 response)
