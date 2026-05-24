import argparse
import json
from typing import Any, Dict, Union


def calculate_progress(completed: Union[int, float], total: Union[int, float]) -> Dict[str, Any]:
    """Return progress summary as a JSON-serializable dictionary."""
    if not isinstance(completed, (int, float)) or not isinstance(total, (int, float)):
        raise TypeError("completed and total must be numeric")

    if total == 0:
        raise ValueError("total must be greater than zero")

    if completed < 0 or total < 0:
        raise ValueError("completed and total must be non-negative")

    progress = (completed / total) * 100
    progress = max(0.0, min(progress, 100.0))

    return {
        "completed": completed,
        "total": total,
        "progress_percent": round(progress, 2),
    }


def progress_json(completed: Union[int, float], total: Union[int, float]) -> str:
    """Return progress result as a JSON string."""
    return json.dumps(calculate_progress(completed, total))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate progress percentage from completed and total values."
    )
    parser.add_argument("completed", type=float, help="Number of completed items")
    parser.add_argument("total", type=float, help="Total number of items")

    args = parser.parse_args()
    print(progress_json(args.completed, args.total))
