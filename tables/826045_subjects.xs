table subjects {
  auth = false

  schema {
    // Unique identifier for the subject
    int id
  
    // ID of the user who owns this subject
    int user_id {
      table = "user"
    }
  
    // Name of the subject
    text name filters=trim
  
    // Subject code, optional legacy identifier (max 20 characters)
    text code? filters=trim|max:20

    // Professor responsible for this subject
    text professor filters=trim

    // Total workload in hours
    int workload_hours filters=min:1
  
    // Academic semester or period (optional)
    text semester? filters=trim

    // Whether the subject was archived instead of deleted
    bool archived?=false
  
    // Optional description of the subject
    text description? filters=trim
  
    // Creation timestamp in RFC3339 format
    timestamp created_at?=now
  
    // Last update timestamp in RFC3339 format
    timestamp updated_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {
      type : "btree|unique"
      field: [
        {name: "user_id", op: "asc"}
        {name: "name", op: "asc"}
        {name: "professor", op: "asc"}
      ]
    }
    {type: "btree", field: [{name: "archived", op: "asc"}]}
  ]
  guid = "5LgWbN63BdHDCIEzFCrf9YcxDUc"
}
