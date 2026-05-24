// Delete a subject owned by the authenticated user.
query "subjects/{id}" verb=DELETE {
  api_group = "subjects"
  auth = "user"

  input {
    // Subject ID to delete.
    int id
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found"
    }

    db.del subjects {
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
}
