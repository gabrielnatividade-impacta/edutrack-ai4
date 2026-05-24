// Search subjects with optional filters for name and overdue tasks
// Returns subjects enriched with overdue task count and list of overdue tasks
query "subjects/search" verb=GET {
  api_group = "F-5n_QXm"
  auth = "user"

  input {
    text? name
    bool? has_overdue
  }

  stack {
    // Query subjects for the authenticated user
    db.query academic_subjects {
      where = user_id == $auth.id
      sort = name asc
      return = {type: "list"}
      output = [
        "id"
        "name"
        "code"
        "description"
        "status"
        "user_id"
        "created_at"
        "updated_at"
      ]
    } as $subjects

    // Filter by name if provided (case-insensitive)
    var $filtered_subjects {
      value = if($input.name && $input.name | length > 0)
        then $subjects | filter:item:$item.name | lower | contains($input.name | lower)
        else $subjects
    }

    // Enrich each subject with overdue count and tasks by iterating and building result
    var $enriched_subjects {
      value = []
    }

    foreach ($filtered_subjects) as $subject {
      // Call the helper function to get overdue data
      call function("Search Helpers/calculate_overdue_count") {
        subject_id: $subject.id
      } as $overdue_data

      // Build enriched subject object with overdue information
      var $enriched_subject {
        value = {
          id: $subject.id
          name: $subject.name
          code: $subject.code
          description: $subject.description
          status: $subject.status
          user_id: $subject.user_id
          overdue_count: $overdue_data.overdue_count
          overdue_tasks: $overdue_data.overdue_tasks
        }
      }

      // Add enriched subject to results array
      var $enriched_subjects {
        value = $enriched_subjects | append($enriched_subject)
      }
    }

    // Filter by has_overdue if requested
    var $final_subjects {
      value = if($input.has_overdue == true)
        then $enriched_subjects | filter:item:$item.overdue_count > 0
        else $enriched_subjects
    }
  }

  response = $final_subjects
  tags = ["xano:quick-start"]
}
