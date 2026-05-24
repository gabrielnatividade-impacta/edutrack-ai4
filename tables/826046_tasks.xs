table tasks {
  auth = false

  schema {
    // Unique identifier for the task
    int id

    // ID of the subject this task belongs to
    int subject_id {
      table = "subjects"
    }

    // ID of the user who owns this task
    int user_id {
      table = "user"
    }

    // Title/name of the task
    text title filters=trim

    // Optional detailed description of the task
    text description? filters=trim

    // Due date for the task
    timestamp due_date

    // Task priority: low, medium, or high
    text priority? filters=trim default="medium"

    // Task status: pending, in_progress, or completed
    text status? filters=trim default="pending"

    // Creation timestamp
    timestamp created_at?=now

    // Last update timestamp
    timestamp updated_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
    {
      type: "btree"
      field: [
        {name: "subject_id", op: "asc"}
        {name: "due_date", op: "asc"}
      ]
    }
    {type: "btree", field: [{name: "status", op: "asc"}]}
    {type: "btree", field: [{name: "priority", op: "asc"}]}
  ]
  guid = "OFIyMByHf76wE6TGrF6G9rA6c4w"
}
