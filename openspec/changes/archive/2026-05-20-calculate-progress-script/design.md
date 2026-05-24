## Context

EduTrack needs a simple Python utility that calculates task completion progress and returns the result in JSON format. This change adds a reusable module and command-line interface so the feature can be consumed both programmatically and from scripts.

## Decisions

- Use Python standard library only: `json`, `argparse`, and type validation.
- Expose a module function `calculate_progress(completed, total)` for imports.
- Provide a CLI entry point that prints JSON output.
- Validate inputs to avoid division by zero and invalid numeric values.
- Return `progress_percent` as a float rounded to two decimals.
- Clamp percentage to the range 0-100 for any out-of-range completed values.

## Design

- `scripts/calculate_progress.py` will define:
  - `calculate_progress(completed, total)` returning a JSON-serializable dict
  - `progress_json(completed, total)` returning a JSON string
  - a CLI entry point using `argparse`
- The JSON result will include:
  - `completed`
  - `total`
  - `progress_percent`

## Validation

- `total` must be greater than zero.
- `completed` and `total` must be numeric values.
- Negative values are rejected.

## Testing

- Add unit tests for normal percentage calculation
- Add tests for zero/negative inputs and CLI JSON output
