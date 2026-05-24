// Update a task owned by the authenticated user.
query "tasks/{id}" verb=PUT {
  api_group = "tasks"
  auth = "user"

  input {
    int id
    int subject_id?
    text title? filters=trim
    text description? filters=trim
    timestamp due_date?
    text status? filters=trim
    text priority? filters=trim
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

    conditional {
      if ($input.subject_id != null) {
        db.get subjects {
          field_name = "id"
          field_value = $input.subject_id
        } as $subject

        precondition ($subject != null && $subject.user_id == $auth.id) {
          error_type = "notfound"
          error = "Subject not found"
        }
      }
    }

    conditional {
      if ($input.title != null) {
        precondition (($input.title|strlen) > 0) {
          error_type = "inputerror"
          error = "Task title is required"
        }
      }
    }

    conditional {
      if ($input.status != null) {
        precondition ($input.status == "pending" || $input.status == "in_progress" || $input.status == "completed") {
          error_type = "inputerror"
          error = "Invalid status"
        }
      }
    }

    conditional {
      if ($input.priority != null) {
        precondition ($input.priority == "low" || $input.priority == "medium" || $input.priority == "high") {
          error_type = "inputerror"
          error = "Invalid priority"
        }
      }
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
  history = 1000
  guid = "PWndWLy37mKTPjvjU2uokU2M0Ko"
}
