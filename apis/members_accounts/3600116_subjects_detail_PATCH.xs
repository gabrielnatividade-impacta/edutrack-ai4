// Update a subject from the authenticated user's account.
query "subjects/{subject_id}" verb=PATCH {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    int subject_id
    text name? filters=trim
    text code? filters=trim
    text description?
    text professor?
    int workload_hours?
    text semester?
    bool archived?
    bool is_active?
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
        name           : $input.name != null ? $input.name : $subject.name
        code           : $input.code != null ? $input.code : $subject.code
        description    : $input.description != null ? $input.description : $subject.description
        professor      : $input.professor != null ? $input.professor : $subject.professor
        workload_hours : $input.workload_hours != null ? $input.workload_hours : $subject.workload_hours
        semester       : $input.semester != null ? $input.semester : $subject.semester
        archived       : $input.archived != null ? $input.archived : $subject.archived
        updated_at     : now
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["subjects", "update"]
  guid = "l89_1p9M7SLcn0TFqVu238OIlpo"
}
