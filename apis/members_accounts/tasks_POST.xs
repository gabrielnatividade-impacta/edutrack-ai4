// Create an academic task linked to a subject in the authenticated user's account.
query "tasks" verb=POST {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int subject_id
    text title filters=trim
    text description? filters=trim
    date due_date?
    text status? filters=trim
    text priority? filters=trim
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_id"]
    } as $user

    precondition ($user.id == $auth.id) {
      error_type = "accessdenied"
      error = "User not found"
    }

    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
      output = ["id", "user_id", "archived"]
    } as $subject

    precondition ($subject.id != null && $subject.user_id == $auth.id && $subject.archived != true) {
      error_type = "notfound"
      error = "Subject not found"
    }

    precondition (($input.title|strlen) > 0) {
      error_type = "badrequest"
      error = "Task title is required"
    }

    var $task_status {
      value = $input.status != null ? $input.status : "pending"
    }

    var $task_priority {
      value = $input.priority != null ? $input.priority : "medium"
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
        updated_at : now
      }
    } as $task
  }

  response = $task
  tags = ["tasks", "create"]
  guid = "CWRobSR0yB21so6eOYA6MijBrtI"
}
