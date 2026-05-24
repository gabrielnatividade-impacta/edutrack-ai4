# Subject Management Documentation

This document provides a comprehensive overview of the subject management feature, including the database schema, API endpoints, access control rules, and deployment guide.

## 9.1 Subject Table Schema

The `subject` table stores information about academic subjects.

| Field         | Type      | Description                                                                                               |
|---------------|-----------|-----------------------------------------------------------------------------------------------------------|
| `id`          | `int`     | Unique identifier for the subject.                                                                        |
| `created_at`  | `timestamp`| Timestamp of when the subject was created.                                                                |
| `updated_at`  | `timestamp`| Timestamp of when the subject was last updated.                                                           |
| `account_id`  | `int`     | Foreign key to the `account` table, indicating which account owns the subject. Cascades on delete.          |
| `name`        | `text`    | The name of the subject (e.g., "Mathematics", "Physics").                                                 |
| `code`        | `text`    | The subject code (e.g., "MATH101", "PHYS201"). Unique per account.                                        |
| `description` | `text`    | A detailed description of the subject.                                                                    |
| `credits`     | `numeric` | Number of academic credits for this subject.                                                              |
| `semester`    | `text`    | The semester in which the subject is offered (e.g., "Fall", "Spring").                                    |
| `year`        | `numeric` | The academic year (e.g., 2024, 2025).                                                                     |
| `color`       | `text`    | Optional color for UI display (hex format).                                                               |
| `tags`        | `array`   | Optional tags for categorization and filtering.                                                           |
- `is_active` | `bool` | Flag to indicate if the subject is active (soft delete support). Defaults to `true`. |

## 9.2 Subject API Endpoints

### Create Subject

- **POST** `/api/members_accounts/subjects`
- **Description**: Creates a new subject.
- **Request Body**:
  ```json
  {
    "name": "Introduction to AI",
    "code": "CS50",
    "description": "A foundational course on Artificial Intelligence.",
    "credits": 3,
    "semester": "Fall",
    "year": 2024
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T00:00:00.000Z",
    "account_id": 1,
    "name": "Introduction to AI",
    "code": "cs50",
    "description": "A foundational course on Artificial Intelligence.",
    "credits": 3,
    "semester": "Fall",
    "year": 2024,
    "color": null,
    "tags": null,
    "is_active": true
  }
  ```

### List Subjects

- **GET** `/api/members_accounts/subjects`
- **Description**: Lists subjects for the authenticated user's account.
- **Query Parameters**:
  - `is_active` (bool, optional)
  - `search_term` (text, optional)
  - `sort_by` (text, optional, default: `created_at`)
  - `sort_order` (text, optional, default: `desc`)
  - `limit` (int, optional, default: 50)
  - `offset` (int, optional, default: 0)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Introduction to AI",
      "code": "cs50"
    }
  ]
  ```

### Get Subject

- **GET** `/api/members_accounts/subjects/{id}`
- **Description**: Retrieves a single subject by its ID.
- **Response**:
  ```json
  {
    "id": 1,
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T00:00:00.000Z",
    "account_id": 1,
    "name": "Introduction to AI",
    "code": "cs50",
    "description": "A foundational course on Artificial Intelligence.",
    "credits": 3,
    "semester": "Fall",
    "year": 2024,
    "color": null,
    "tags": null,
    "is_active": true
  }
  ```

### Update Subject

- **PATCH** `/api/members_accounts/subjects/{id}`
- **Description**: Updates a subject's properties.
- **Request Body**:
  ```json
  {
    "description": "An updated description for the AI course."
  }
  ```
- **Response**: The updated subject object.

### Delete Subject

- **DELETE** `/api/members_accounts/subjects/{id}`
- **Description**: Deletes a subject.
- **Response**: `204 No Content`

## 9.3 Access Control Rules

- **Account Owners & Admins**: Can perform all CRUD operations on subjects within their account.
- **Account Members**: Can view subjects.
- **Inactive Subjects**: Only visible to Account Owners and Admins.

## 9.4 Cascade Delete Behavior

When an `account` is deleted, all of its associated `subject` records are automatically deleted from the database. This is enforced by a `cascade` delete constraint on the `account_id` foreign key in the `subject` table.

## 9.5 Migration Guide

This is a new feature, so no data migration is required. To deploy this change:

1.  Run the database schema migration to create the `subject` table.
2.  Deploy the new API endpoints and functions.
3.  The new `query_subjects` function should be used for fetching subjects to ensure performance.
