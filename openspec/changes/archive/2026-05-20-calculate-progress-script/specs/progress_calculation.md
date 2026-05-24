## Progress Calculation

- [x] 1.1 Calculate `progress_percent` as `(completed / total) * 100`
- [x] 1.2 Return `completed`, `total`, and `progress_percent` in JSON format
- [x] 1.3 Round `progress_percent` to two decimal places
- [x] 1.4 Clamp `progress_percent` to the range 0-100

## Validation

- [x] 2.1 Reject `total` when it is zero
- [x] 2.2 Reject negative `completed` or `total` values
- [x] 2.3 Reject non-numeric inputs for `completed` and `total`

## Runtime Behavior

- [x] 3.1 Support importing the module and calling `calculate_progress`
- [x] 3.2 Support command-line execution with `argparse`
- [x] 3.3 Print valid JSON to stdout when executed as a script
