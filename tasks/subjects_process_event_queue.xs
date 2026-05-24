task "subjects_process_event_queue" {
  description = "Process pending subject event queue entries and write them to the event_log table."

  stack {
    db.query subject_event_queue {
      where = $db.subject_event_queue.status == "pending"
      sort = {subject_event_queue.created_at: "asc"}
      return = {type: "list"}
    } as $pending_events

    foreach ($pending_events) {
      each as $queued_event {
        try_catch {
          try {
            function.run "subjects/log_subject_event" {
              input = {
                action    : $queued_event.action
                user_id   : $queued_event.user_id
                subject_id: $queued_event.subject_id
                details   : $queued_event.details
              }
            } as $log_result

            db.patch subject_event_queue {
              field_name = "id"
              field_value = $queued_event.id
              data = {
                status       : "processed"
                processed_at : now
                error_message: null
              }
            }
          }

          catch {
            db.patch subject_event_queue {
              field_name = "id"
              field_value = $queued_event.id
              data = {
                status       : "failed"
                processed_at : now
                error_message: $error
              }
            }
          }
        }
      }
    }
  }
}
