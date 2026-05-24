query test verb=POST {
  api_group = "test"

  input {
    text name
  }

  stack {
    db.add "" {
      data = {name: $input.name}
    } as $new_test
  }

  response = $new_test
}