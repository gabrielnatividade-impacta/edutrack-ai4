## 1. Database Schema Setup

- [x] 1.1 Verify subjects table exists and has id field
- [x] 1.2 Create academic_tasks table with fields: id (primary key), title (text), description (text), due_date (date), status (text)
- [x] 1.3 Add foreign key relationship: subject_id references subjects.id with cascade delete

## 2. Validation and Testing

- [x] 2.1 Test table creation and relationships
- [x] 2.2 Verify data integrity constraints work correctly
- [x] 2.3 Push changes to Xano backend using xano.xanoscript/push_all_changes_to_xano tool