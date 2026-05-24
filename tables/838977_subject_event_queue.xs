// Queue table for subject event logging tasks.
table subject_event_queue {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int user_id {
      table = "user"
    }
  
    text action? filters=trim
    int subject_id?
    json details?
    text status?=pending filters=trim
    timestamp processed_at?
    text error_message? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "status"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["xano:subjects"]
}