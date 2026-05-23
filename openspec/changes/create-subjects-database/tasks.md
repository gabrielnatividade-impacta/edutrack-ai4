## 1. Database Schema Creation

- [x] 1.1 Create subject table with all required fields (id, account_id, name, code, description, credits, semester, year, color, tags, is_active, created_at, updated_at)
- [x] 1.2 Set up foreign key constraint from subject.account_id to account.id with cascade delete behavior
- [x] 1.3 Create unique constraint on (account_id, code) to ensure code uniqueness per account
- [x] 1.4 Add database indexes on account_id, is_active, and created_at fields for query performance
- [x] 1.5 Verify table structure and relationships are correctly created in database

## 2. API Endpoints - Core CRUD Operations

- [x] 2.1 Create POST /api/members_accounts/subjects endpoint to create new subjects with account ownership validation
- [x] 2.2 Create GET /api/members_accounts/subjects endpoint to list subjects with account filtering and pagination support
- [x] 2.3 Create GET /api/members_accounts/subjects/{id} endpoint to retrieve single subject with access control check
- [x] 2.4 Create PATCH /api/members_accounts/subjects/{id} endpoint to update subject properties with authorization check
- [x] 2.5 Create DELETE /api/members_accounts/subjects/{id} endpoint for subject deletion with access control

## 3. Access Control Integration

- [x] 3.1 Integrate role_based_access_control function into subject creation endpoint (account owner and admin only)
- [x] 3.2 Integrate RBAC into subject read endpoints (all account members can view, based on role visibility rules)
- [x] 3.3 Integrate RBAC into subject update endpoint (owner and admin can edit, members cannot)
- [x] 3.4 Integrate RBAC into subject deletion endpoint (owner and admin only)
- [x] 3.5 Add account membership verification before any subject access (ensure user belongs to owning account)
- [x] 3.6 Implement visibility logic for is_active flag (admins/owners see inactive subjects, others see only active)

## 4. Input Validation and Error Handling

- [x] 4.1 Add validation for required fields (name, code, account_id) with appropriate error messages
- [x] 4.2 Add field type validation (name/code/description as strings, credits/year as numeric, color as hex format)
- [x] 4.3 Add field length validation (name max 255, code max 50, description max 1000)
- [x] 4.4 Add duplicate code validation within account scope with clear conflict message
- [x] 4.5 Handle and return meaningful error responses for invalid input (400 Bad Request)
- [x] 4.6 Handle and return appropriate errors for access control violations (403 Forbidden)
- [x] 4.7 Handle and return appropriate errors for not found scenarios (404 Not Found)

## 5. Data Integrity and Relationships

- [ ] 5.1 Verify cascade delete works correctly (deleting account removes all subjects)
- [ ] 5.2 Test foreign key constraint enforcement (subject cannot reference non-existent account)
- [ ] 5.3 Verify timestamps (created_at, updated_at) are automatically set and updated
- [ ] 5.4 Test is_active field functionality for soft delete operations
- [ ] 5.5 Verify that all subject queries respect account ownership

## 6. Query and Performance Optimization

- [x] 6.1 Create database addon or query function for efficiently fetching subjects by account_id with filters
- [ ] 6.2 Test query performance with indexes to ensure efficient filtering by account_id and is_active
- [x] 6.3 Implement pagination support for subject list endpoint (limit, offset parameters)
- [x] 6.4 Add sorting support for subject lists (by name, code, created_at, etc.)
- [ ] 6.5 Test N+1 query prevention when loading multiple subjects with account context

## 7. Event Logging Integration (Future Enhancement)

- [x] 7.1 Plan event logging structure for subject operations (create_subject, update_subject, delete_subject)
- [x] 7.2 Document how future event logging will integrate with subject CRUD operations
- [x] 7.3 Ensure subject table structure supports event logging extensibility

## 8. Testing and Validation

- [ ] 8.1 Write unit tests for subject creation with various field combinations
- [ ] 8.2 Write unit tests for subject retrieval (single and list) with access control validation
- [ ] 8.3 Write unit tests for subject update with permission checks
- [ ] 8.4 Write unit tests for subject deletion with access control enforcement
- [ ] 8.5 Write integration tests for cascade delete behavior (account deletion removes subjects)
- [ ] 8.6 Test access control scenarios (cross-account access prevention, role-based permissions)
- [ ] 8.7 Test validation error handling for invalid inputs
- [ ] 8.8 Test unique constraint violation when creating duplicate subject codes

## 9. Documentation and Deployment

- [x] 9.1 Document subject table schema and fields in developer documentation
- [x] 9.2 Document subject API endpoints with request/response examples
- [x] 9.3 Document access control rules for subject operations
- [x] 9.4 Document cascade delete behavior and implications
- [x] 9.5 Create migration guide for deploying subject database changes
- [ ] 9.6 Verify backward compatibility with existing account and user systems
- [ ] 9.7 Deploy subject table to production environment
- [ ] 9.8 Run validation tests against production database to confirm all requirements are met

## 10. Future Extensibility Preparation

- [x] 10.1 Document how subject-level event logging can be added without schema changes
- [x] 10.2 Document how explicit enrollment tracking can be implemented in future
- [ ] 10.3 Verify account-subject relationship supports team collaboration patterns
- [x] 10.4 Document open questions (e.g., cross-account subject sharing if needed in future)
