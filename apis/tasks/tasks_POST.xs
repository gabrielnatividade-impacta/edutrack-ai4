// Create a task linked to one of the authenticated user's subjects.
query "tasks" verb=POST {
  api_group = "tasks"
  auth = "user"

  input {
    int subject_id
    text title filters=trim
    text description? filters=trim
    timestamp due_date
    text status? filters=trim
    text priority? filters=trim
  }

  stack {
    precondition (($input.title|strlen) > 0) {
      error_type = "inputerror"
      error = "Task title is required"
    }

    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found"
    }

    var $task_status {
      value = $input.status != null ? $input.status : "pending"
    }

    var $task_priority {
      value = $input.priority != null ? $input.priority : "medium"
    }

    precondition ($task_status == "pending" || $task_status == "in_progress" || $task_status == "completed") {
      error_type = "inputerror"
      error = "Invalid status"
    }

    precondition ($task_priority == "low" || $task_priority == "medium" || $task_priority == "high") {
      error_type = "inputerror"
      error = "Invalid priority"
    }

    db.add tasks {
      data = {
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $task_status
        priority   : $task_priority
        created_at : now
        updated_at : now
      }
    } as $task

    util.set_header {
      value = "HTTP/1.1 201 Created"
      duplicates = "replace"
    }
  }

  response = $task
  history = 1000
  guid = "z1J7lyzxG61w66Jpg0KKWbCaOlw"
}
