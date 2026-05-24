// Stores academic subjects for users
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // The name of the subject (e.g., "Introduction to AI")
    text name filters=trim
  
    // An optional code for the subject (e.g., "CS101")
    text code?
  
    // A longer description of the subject
    text description?

    // Professor responsible for this subject
    text professor? filters=trim

    // Total workload in hours
    int workload_hours?

    // Academic semester or period
    text semester? filters=trim

    // Active flag used for archiving without deleting
    bool is_active?=true

    // Timestamp of the last update
    timestamp updated_at?
  
    // The status of the subject record
    enum status? {
      values = ["active", "archived"]
    }
  
    // Reference to the user who owns this subject
    int user_id {
      table = "user"
    }
  
    // Reference to the account this subject belongs to
    int account_id {
      table = "account"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "account_id"}]}
  ]

  tags = ["edutrack"]
  guid = "2GZX1JZAzPVvHnyrds8PosgT2BA"
}
