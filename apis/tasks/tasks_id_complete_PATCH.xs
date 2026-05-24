// Mark a task owned by the authenticated user as completed.
query "tasks/{id}/complete" verb=PATCH {
  api_group = "tasks"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get tasks {
      field_name = "id"
      field_value = $input.id
    } as $task

    precondition ($task != null && $task.user_id == $auth.id) {
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
  history = 1000
  guid = "cbhs0HG8pG7ObNGhrut_ZybnGGE"
}
