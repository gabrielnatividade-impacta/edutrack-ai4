// Create a new subject associated with the authenticated user's account.
query "subjects" verb=POST {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    text name filters=trim
    text code filters=trim
    text description?
    text professor?
    int workload_hours?
    text semester?
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "account_id", "role"]
    } as $user

    precondition ($user.id == $auth.id) {
      error_type = "accessdenied"
      error = "User not found"
    }

    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      sort = {subjects.created_at: "desc"}
      return = {type: "list"}
    } as $existing_subjects

    var $duplicate_count {
      value = 0
    }

    foreach ($existing_subjects) {
      each as $existing_subject {
        conditional {
          if ($existing_subject.name == $input.name) {
            conditional {
              if ($existing_subject.professor == $input.professor) {
                conditional {
                  if ($existing_subject.archived != true) {
                    var.update $duplicate_count {
                      value = $duplicate_count + 1
                    }
                  }
                }
              }
            }
          }
        }
      }
    }

    precondition ($duplicate_count == 0) {
      error_type = "badrequest"
      error = "Subject already exists for this professor"
    }

    db.add subjects {
      data = {
        user_id        : $auth.id
        name           : $input.name
        code           : $input.code
        description    : $input.description
        professor      : $input.professor
        workload_hours : $input.workload_hours
        semester       : $input.semester
        archived       : false
        updated_at     : now
      }
    } as $subject
  }

  response = $subject
  tags = ["subjects", "create"]
  guid = "5XECFa0c3bHZFw9rp8w_Uutmm2Q"
}
