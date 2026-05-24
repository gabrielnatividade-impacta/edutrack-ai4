// Update an academic task owned by the authenticated user.
query "tasks/{id}" verb=PUT {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int id
    int subject_id?
    text title? filters=trim
    text description? filters=trim
    date due_date?
    text status? filters=trim
    text priority? filters=trim
  }

  stack {
    db.get tasks {
      field_name = "id"
      field_value = $input.id
    } as $task

    precondition ($task.id != null && $task.user_id == $auth.id) {
      error_type = "notfound"
      error = "Task not found"
    }

    db.edit tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        subject_id : $input.subject_id != null ? $input.subject_id : $task.subject_id
        title      : $input.title != null ? $input.title : $task.title
        description: $input.description != null ? $input.description : $task.description
        due_date   : $input.due_date != null ? $input.due_date : $task.due_date
        status     : $input.status != null ? $input.status : $task.status
        priority   : $input.priority != null ? $input.priority : $task.priority
        updated_at : now
      }
    } as $updated_task
  }

  response = $updated_task
  tags = ["tasks", "update"]
  guid = "hQBexe5i3rHz-1-t-m0lFnawMso"
}
