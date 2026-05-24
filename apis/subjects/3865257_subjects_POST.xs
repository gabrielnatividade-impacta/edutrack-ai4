// Create a new subject for the authenticated user.
query "subjects" verb=POST {
  api_group = "subjects"
  description = "Create a new subject for the authenticated user with name, professor, workload, and optional semester/description"
  auth = "user"

  input {
    // Subject name.
    text name filters=trim

    // Optional subject code, max 20 characters.
    text code? filters=trim|max:20

    // Professor responsible for this subject.
    text professor filters=trim

    // Total workload in hours.
    int workload_hours filters=min:1

    // Academic semester or period.
    text semester? filters=trim

    // Optional description of the subject.
    text description? filters=trim
  }

  stack {
    precondition (($input.name|strlen) > 0) {
      error_type = "inputerror"
      error = "Subject name is required"
    }

    precondition (($input.professor|strlen) > 0) {
      error_type = "inputerror"
      error = "Professor is required"
    }

    db.query subjects {
      where = $db.subjects.name == $input.name
        && $db.subjects.professor == $input.professor
        && $db.subjects.user_id == $auth.id
        && $db.subjects.archived != true
      return = {type: "list"}
    } as $existing_subjects

    precondition (($existing_subjects|count) == 0) {
      error_type = "inputerror"
      error = "Subject already exists for this professor"
    }

    db.add subjects {
      data = {
        user_id    : $auth.id
        name       : $input.name
        code       : $input.code
        professor  : $input.professor
        workload_hours: $input.workload_hours
        semester   : $input.semester
        description: $input.description
        archived   : false
        created_at : now
        updated_at : now
      }
    } as $new_subject

    util.set_header {
      value = "HTTP/1.1 201 Created"
      duplicates = "replace"
    }
  }

  response = $new_subject
  history = 1000
}
