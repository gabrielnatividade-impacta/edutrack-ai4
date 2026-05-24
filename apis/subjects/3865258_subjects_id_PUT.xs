// Update an existing subject owned by the authenticated user.
query "subjects/{id}" verb=PUT {
  api_group = "subjects"
  auth = "user"

  input {
    // Subject ID to update.
    int id

    // Updated subject name.
    text name? filters=trim

    // Updated subject code, max 20 characters.
    text code? filters=trim|max:20

    // Updated professor name.
    text professor? filters=trim

    // Updated workload in hours.
    int workload_hours? filters=min:1

    // Updated academic semester or period.
    text semester? filters=trim

    // Updated subject description.
    text description? filters=trim

    // Archived flag for completed subjects.
    bool archived?
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

    var $next_name {
      value = $input.name != null ? $input.name : $subject.name
    }

    var $next_professor {
      value = $input.professor != null ? $input.professor : $subject.professor
    }

    db.query subjects {
      where = $db.subjects.name == $next_name
        && $db.subjects.professor == $next_professor
        && $db.subjects.user_id == $auth.id
        && $db.subjects.id != $input.id
        && $db.subjects.archived != true
      return = {type: "list"}
    } as $existing_subjects

    precondition (($existing_subjects|count) == 0) {
      error_type = "inputerror"
      error = "Subject already exists for this professor"
    }

    conditional {
      if ($input.name != null) {
        precondition (($input.name|strlen) > 0) {
          error_type = "inputerror"
          error = "Subject name is required"
        }
      }
    }

    conditional {
      if ($input.professor != null) {
        precondition (($input.professor|strlen) > 0) {
          error_type = "inputerror"
          error = "Professor is required"
        }
      }
    }

    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name       : $input.name != null ? $input.name : $subject.name
        code       : $input.code != null ? $input.code : $subject.code
        professor  : $input.professor != null ? $input.professor : $subject.professor
        workload_hours: $input.workload_hours != null ? $input.workload_hours : $subject.workload_hours
        semester   : $input.semester != null ? $input.semester : $subject.semester
        description: $input.description != null ? $input.description : $subject.description
        archived   : $input.archived != null ? $input.archived : $subject.archived
        updated_at : now
      }
    } as $updated_subject
  }

  response = $updated_subject
  history = 1000
}
