table academic_tasks {
  auth = false

  schema {
    // Unique identifier for the academic task
    int id

    // ID of the user who owns this task
    int user_id {
      table = "user"
    }

    // ID of the subject this task belongs to
    int subject_id {
      table = "subjects"
    }

    // Title of the academic task
    text title filters=trim

    // Description of the academic task
    text description? filters=trim

    // Due date for the academic task
    timestamp due_date

    // Status of the academic task
    text status? filters=trim default="pending"

    // Priority of the academic task
    text priority? filters=trim default="medium"

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
    {type: "btree", field: [{name: "status", op: "asc"}]}
    {type: "btree", field: [{name: "priority", op: "asc"}]}
  ]
}
