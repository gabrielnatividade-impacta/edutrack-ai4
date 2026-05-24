// Stores academic tasks associated with subjects and users
table academic_task {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // Timestamp of the last update to the task.
    timestamp updated_at?
  
    // Reference to the account that owns this task.
    int account? {
      table = "account"
    }
  
    // Reference to the user that owns this task.
    int user? {
      table = "user"
    }
  
    // Reference to the subject this task belongs to.
    int subject? {
      table = "subject"
    }
  
    // Title of the academic task
    text title? filters=trim
  
    // Description of the academic task
    text description? filters=trim
  
    // Due date of the task
    date due_date?
  
    // Status of the task (e.g., pending, completed)
    text status? filters=trim

    // Priority of the task (low, medium, or high)
    text priority? filters=trim
  
    // Active flag (soft delete support)
    bool is_active?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
  guid = "zgQGW7Xpyyu3-2gbvmrH9WPLmrY"
}
