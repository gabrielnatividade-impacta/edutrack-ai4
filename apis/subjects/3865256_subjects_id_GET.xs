// Retrieve a single subject by ID.
// Authenticated users can only view subjects they own.
query "subjects/{id}" verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    // Subject ID to retrieve.
    int id
  }

  stack {
    db.query subjects {
      where = $db.subjects.id == $input.id && $db.subjects.user_id == $auth.id
      return = {type: "single"}
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found"
    }
  }

  response = $subject
  history = 100
}
