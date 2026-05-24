// Mark an academic task owned by the authenticated user as completed.
query "tasks/{id}/complete" verb=PATCH {
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

    db.edit tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        status    : "completed"
        updated_at: now
      }
    } as $updated_task
  }

  response = $updated_task
  tags = ["tasks", "complete"]
  guid = "wN2dXfxhDLGQeKDB3CP8XKR7rxA"
}
