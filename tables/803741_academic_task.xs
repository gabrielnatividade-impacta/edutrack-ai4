// Stores academic tasks associated with subjects and users
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    timestamp updated_at?=now

    // Reference to the account that owns this task
    int account_id? {
      table = "account"
    }

    // Reference to the user that owns this task
    int user_id? {
      table = "user"
    }

    // Reference to the subject this task belongs to
    int subject_id? {
      table = "subject"
    }

    // Title of the academic task
    text title filters=trim

    // Description of the academic task
    text description? filters=trim

    // Due date of the task
    date due_date?

    // Status of the task (e.g., pending, completed)
    text status?="pending" filters=trim|lower

    // Active flag (soft delete support)
    bool is_active?=true
  }

  index = [
    {type: "primary", field: [{name: "id"}]},
    {type: "btree", field: [{name: "account_id", op: "asc"}]},
    {type: "btree", field: [{name: "user_id", op: "asc"}]},
    {type: "btree", field: [{name: "subject_id", op: "asc"}]},
    {type: "btree", field: [{name: "is_active", op: "asc"}]},
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
  ]

  tags = ["edutrack-ai"]
}