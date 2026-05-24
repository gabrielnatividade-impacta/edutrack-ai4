// Calculates the number of overdue tasks for a given subject
// An overdue task is defined as:
//   - due_date is in the past (< now)
//   - status is not "completed"
//
function "Search Helpers/calculate_overdue_count" {
  input {
    // UUID of the subject to calculate overdue tasks for
    uuid subject_id
  }

  stack {
    // Query all academic tasks for this subject that are overdue and not completed
    db.query academic_tasks {
      filter = subject_id == $input.subject_id && due_date < now() && status != "completed"
      sort = due_date desc
    } as $overdue_tasks

    // Calculate overdue count
    var $overdue_count {
      value = $overdue_tasks|count
    }

    // Map overdue tasks to response format
    var $mapped_overdue_tasks {
      value = $overdue_tasks|map:item:{id: $item.id, title: $item.title, due_date: $item.due_date, status: $item.status}
    }
  }

  // Build response with count and list of overdue tasks
  response = {
    overdue_count: $overdue_count
    overdue_tasks: $mapped_overdue_tasks
  }
}
