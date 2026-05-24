// Enqueue a subject event for asynchronous processing.
// This helper adds a queue record and triggers the background event processor.
function "subjects/enqueue_subject_event" {
  input {
    // Event type - must be one of the valid subject event actions.
    text action filters=trim
  
    // ID of user performing the action.
    int user_id
  
    // ID of subject affected, optional for access denied events.
    int subject_id?
  
    // Additional context for the event.
    json details?
  }

  stack {
    var $valid_actions {
      value = [
        "subject_created"
        "subject_updated"
        "subject_deleted"
        "subject_access_denied"
      ]
    }
  
    precondition ($valid_actions|in:$input.action) {
      error_type = "inputerror"
      error = "Invalid action. Must be one of: subject_created, subject_updated, subject_deleted, subject_access_denied"
    }
  
    db.add subject_event_queue {
      data = {
        user_id      : $input.user_id
        action       : $input.action
        subject_id   : $input.subject_id
        details      : $input.details
        created_at   : now
        status       : "pending"
        processed_at : null
        error_message: null
      }
    } as $queue_item
  
    task.call "" as $task_trigger
  }

  response = {queued: true, queue_id: $queue_item.id}
}