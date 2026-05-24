// Search subjects by name OR overdue task status
query "subjects/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text name? filters=trim
    bool hasOverdueTasks?
    bool archived?=false
    int limit?=50 filters=min:1|max:100
    int offset?=0 filters=min:0
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
        && ($db.subjects.archived ==? $input.archived)
      sort = {subjects.created_at: "desc"}
      return = {
        type: "list"
        paging: {
          page: 1
          per_page: $input.limit
          offset: $input.offset
          totals: true
        }
      }
    } as $subjects

    var $filtered_subjects {
      value = []
    }

    foreach ($subjects) {
      each as $subject {
        db.query tasks {
          where = $db.tasks.subject_id == $subject.id
            && $db.tasks.user_id == $auth.id
            && $db.tasks.status != "completed"
            && $db.tasks.due_date < now
          return = {type: "list"}
        } as $overdue_tasks

        var $overdue_count {
          value = $overdue_tasks|count
        }

        var $has_overdue {
          value = $overdue_count > 0
        }

        var $name_matches {
          value = true
        }

        conditional {
          if ($input.name != null && ($input.name|strlen) > 0) {
            var.update $name_matches {
              value = ($subject.name|lower)|contains:($input.name|lower)
            }
          }
        }

        var $overdue_matches {
          value = true
        }

        conditional {
          if ($input.hasOverdueTasks != null) {
            var.update $overdue_matches {
              value = $has_overdue == $input.hasOverdueTasks
            }
          }
        }

        conditional {
          if ($name_matches || $overdue_matches) {
            var.update $filtered_subjects {
              value = $filtered_subjects|push:{
                id: $subject.id
                name: $subject.name
                code: $subject.code
                professor: $subject.professor
                workload_hours: $subject.workload_hours
                semester: $subject.semester
                description: $subject.description
                archived: $subject.archived
                created_at: $subject.created_at
                updated_at: $subject.updated_at
                overdue_task_count: $overdue_count
                has_overdue_tasks: $has_overdue
              }
            }
          }
        }
      }
    }
  }

  response = {
    data: $filtered_subjects
    count: $filtered_subjects|count
  }

  history = 100
}
