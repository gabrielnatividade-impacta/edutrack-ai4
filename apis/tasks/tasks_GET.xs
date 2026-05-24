// List authenticated user's tasks with optional status, subject, and grouping filters.
query "tasks" verb=GET {
  api_group = "tasks"
  auth = "user"

  input {
    int subject_id?
    text status? filters=trim
    text group_by? filters=trim
    int limit?=100 filters=min:1|max:200
    int offset?=0 filters=min:0
  }

  stack {
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

  response = {
    group_by: $input.group_by
    data: $tasks
  }
  history = 100
  guid = "viSt3oS1pbc-Q9P24AD2zefRztM"
}
