// List all subjects for authenticated user.
// Supports optional pagination, semester, and archived filtering.
query "subjects" verb=GET {
  api_group = "subjects"
  description = "List all subjects for authenticated user with optional pagination, semester, and archived filtering"
  auth = "user"

  input {
    // Number of subjects to return (default 50, max 100)
    int limit?=50 filters=min:1|max:100
  
    // Number of subjects to skip for pagination (default 0)
    int offset? filters=min:0
  
    // Optional semester filter to retrieve only subjects from a specific semester
    text semester? filters=trim

    // Optional archived filter; defaults to active subjects only
    bool archived?=false
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
        && ($db.subjects.semester ==? $input.semester)
        && ($db.subjects.archived ==? $input.archived)
      sort = {subjects.created_at: "desc"}
      return = {
        type  : "list"
        paging: {
          page    : 1
          per_page: $input.limit
          totals  : true
          offset  : $input.offset
        }
      }
    } as $subjects
  }

  response = $subjects
  history = 100
}
