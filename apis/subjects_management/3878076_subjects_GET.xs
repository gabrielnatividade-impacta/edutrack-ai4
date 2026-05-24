// List subjects owned by the authenticated user.
query subjects verb=GET {
  api_group = "Subjects Management"
  auth = "user"

  input {
  }

  stack {
    db.query "" {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  tags = ["xano:quick-start"]
}