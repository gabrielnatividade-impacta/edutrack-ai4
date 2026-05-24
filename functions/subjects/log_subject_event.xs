// Log subject-related events to the event_log table for audit trail. Records all subject operations (created, updated, deleted, access_denied) with optional context details.
function "subjects/log_subject_event" {
  input {
    // Event type - must be one of: subject_created, subject_updated, subject_deleted, subject_access_denied
    text action filters=trim
  
    // ID of user performing the action
    int user_id
  
    // ID of subject affected (optional, null for access_denied events where subject doesn't exist)
    int subject_id?
  
    // Additional context for the event (changed_fields array and/or error_message string)
    json details?
  }

  stack {
    // Build metadata object with subject context
    var $metadata = {
      subject_id: $input.subject_id,
      changed_fields: if ($input.details != null) { $input.details.changed_fields } else { null },
      error_message: if ($input.details != null) { $input.details.error_message } else { null },
      operation: if ($input.details != null) { $input.details.operation } else { null }
    }

    // Add event to event_log with error handling
    var $event_result = null

    try_catch {
      try {
        // Create event log entry for subject operation
        db.add event_log {
          data = {
            created_at: "now",
            user_id: $input.user_id,
            action: $input.action,
            metadata: $metadata
          }
        } as $event_result
      }

      catch {
        // Set to null on error to indicate logging failure
        $event_result = null
      }
    }
  }

  response = {
    success: ($event_result != null),
    event_id: if ($event_result != null) { $event_result.id } else { null },
    error: if ($event_result == null) { "Failed to log event" } else { null }
  }
}