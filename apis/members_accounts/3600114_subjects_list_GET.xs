// List subjects for the authenticated user's account.
query "subjects" verb=GET {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int limit?=100
    int offset?=0
    bool include_inactive?=false
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

    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      sort = {subjects.created_at: "desc"}
      return = {type: "list"}
    } as $subjects
  }

  response = {
    subjects: $subjects
    limit: $input.limit
    offset: $input.offset
  }
  tags = ["subjects", "list"]
  guid = "5lFV1ic1gfPuGT3WkURN48KoKK4"
}
