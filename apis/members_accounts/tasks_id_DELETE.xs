// Delete an academic task owned by the authenticated user.
query "tasks/{id}" verb=DELETE {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int id
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

    db.del tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
    task_id: $input.id
  }
  tags = ["tasks", "delete"]
  guid = "dmh1bK4WQ59kU91bO6j7SBqygRo"
}
