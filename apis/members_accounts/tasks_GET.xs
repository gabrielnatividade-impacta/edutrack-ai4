// List academic tasks for the authenticated user.
query "tasks" verb=GET {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int subject_id?
    text status? filters=trim
    int limit?=100
    int offset?=0
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

    db.query tasks {
      where = $db.tasks.user_id == $auth.id
      sort = {tasks.due_date: "asc"}
      return = {
        type: "list"
        paging: {
          page: 1
          per_page: $input.limit
          offset: $input.offset
          totals: true
        }
      }
    } as $tasks
  }

  response = $tasks
  tags = ["tasks", "list"]
  guid = "kMrM4ULOAck6f9wKIbss3qwNJTo"
}
