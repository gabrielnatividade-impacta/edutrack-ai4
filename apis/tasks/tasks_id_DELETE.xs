// Delete a task owned by the authenticated user.
query "tasks/{id}" verb=DELETE {
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

    db.del tasks {
      field_name = "id"
      field_value = $input.id
    }

    util.set_header {
      value = "HTTP/1.1 204 No Content"
      duplicates = "replace"
    }
  }

  response = null
  history = 1000
  guid = "2KS_lN7X5yNV2BhSJgy03OuPE1M"
}
