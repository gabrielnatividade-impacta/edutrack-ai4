// Delete a subject from the authenticated user's account.
query "subjects/{subject_id}" verb=DELETE {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int subject_id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_id"]
    } as $user

    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject.id != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found"
    }

    db.edit subjects {
      field_name = "id"
      field_value = $input.subject_id
      data = {
        archived   : true
        updated_at : now
      }
    } as $archived_subject
  }

  response = {
    success: true
    subject_id: $input.subject_id
    subject: $archived_subject
  }
  tags = ["subjects", "delete"]
  guid = "pXJSU-d14pXaMdURcOrsgPoIsHQ"
}
