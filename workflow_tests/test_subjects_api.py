import os
import sys
import requests

BASE_URL = os.environ.get("SUBJECTS_API_BASE_URL", "http://localhost:8000")
USER_A_EMAIL = os.environ.get("USER_A_EMAIL")
USER_A_PASSWORD = os.environ.get("USER_A_PASSWORD")
USER_B_EMAIL = os.environ.get("USER_B_EMAIL")
USER_B_PASSWORD = os.environ.get("USER_B_PASSWORD")


def login(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()["authToken"]


def create_subject(token: str, subject: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}/subjects",
        json=subject,
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def list_subjects(token: str, limit: int = 50, offset: int = 0, semester: str | None = None) -> dict:
    params = {"limit": limit, "offset": offset}
    if semester is not None:
        params["semester"] = semester
    response = requests.get(
        f"{BASE_URL}/subjects",
        params=params,
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def get_subject(token: str, subject_id: int) -> dict:
    response = requests.get(
        f"{BASE_URL}/subjects/{subject_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def update_subject(token: str, subject_id: int, payload: dict) -> dict:
    response = requests.put(
        f"{BASE_URL}/subjects/{subject_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def delete_subject(token: str, subject_id: int) -> requests.Response:
    response = requests.delete(
        f"{BASE_URL}/subjects/{subject_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code not in (204, 404):
        response.raise_for_status()
    return response


def get_user_events(token: str) -> dict:
    response = requests.get(
        f"{BASE_URL}/logs/user/my_events",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def assert_contains_keys(data: dict, keys: list[str]) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        raise AssertionError(f"Missing keys in response: {missing}")


def run_smoke_tests() -> None:
    if not USER_A_EMAIL or not USER_A_PASSWORD or not USER_B_EMAIL or not USER_B_PASSWORD:
        raise RuntimeError(
            "Set USER_A_EMAIL, USER_A_PASSWORD, USER_B_EMAIL, and USER_B_PASSWORD in the environment."
        )

    print("Logging in users...")
    token_a = login(USER_A_EMAIL, USER_A_PASSWORD)
    token_b = login(USER_B_EMAIL, USER_B_PASSWORD)

    print("Creating subject for user A...")
    subject = create_subject(
        token_a,
        {
            "name": "Algebra",
            "code": "ALG101",
            "semester": "2026-1",
            "description": "Fundamentals of algebra",
        },
    )
    assert_contains_keys(subject, ["id", "user_id", "name", "code", "semester", "description", "created_at", "updated_at"])
    subject_id = subject["id"]
    original_user_id = subject["user_id"]

    print("Creating second subject with max length code and optional metadata omitted...")
    second_subject = create_subject(
        token_a,
        {
            "name": "Geometry",
            "code": "GEOMETRYMAXCODE1234",
        },
    )
    assert_contains_keys(second_subject, ["id", "user_id", "name", "code", "created_at", "updated_at"])
    second_subject_id = second_subject["id"]

    print("Validating duplicate code is rejected for same user...")
    try:
        create_subject(
            token_a,
            {
                "name": "Duplicate Algebra",
                "code": "ALG101",
            },
        )
        raise AssertionError("Duplicate subject code should be rejected")
    except requests.HTTPError as exc:
        if exc.response.status_code != 400:
            raise

    print("Validating missing required fields are rejected...")
    for invalid_payload in [{"code": "NO_NAME"}, {"name": "NoCode"}]:
        try:
            create_subject(token_a, invalid_payload)
            raise AssertionError("Missing required fields should be rejected")
        except requests.HTTPError as exc:
            if exc.response.status_code != 400:
                raise

    print("Listing subjects for user A...")
    list_response = list_subjects(token_a)
    if not isinstance(list_response, dict) or "data" not in list_response:
        raise AssertionError("Expected list response to contain a data list")

    print("Retrieving subject by ID for user A...")
    fetched = get_subject(token_a, subject_id)
    assert fetched["id"] == subject_id

    print("Attempting unauthorized access by user B...")
    try:
        get_subject(token_b, subject_id)
        raise AssertionError("User B should not be able to access user A's subject")
    except requests.HTTPError as exc:
        if exc.response.status_code != 404:
            raise

    print("Updating subject for user A and verifying user_id remains immutable...")
    updated = update_subject(token_a, subject_id, {"name": "Advanced Algebra", "semester": "2026-2", "user_id": 9999})
    if updated["name"] != "Advanced Algebra":
        raise AssertionError("Expected updated name to be returned")
    if updated["user_id"] != original_user_id:
        raise AssertionError("user_id should remain unchanged after update")

    print("Attempting unauthorized update by user B...")
    try:
        update_subject(token_b, subject_id, {"name": "Hijacked"})
        raise AssertionError("User B should not be able to update user A's subject")
    except requests.HTTPError as exc:
        if exc.response.status_code != 404:
            raise

    print("Verifying event logs for user A contain subject actions...")
    events = get_user_events(token_a)
    if not isinstance(events, dict) or "data" not in events:
        raise AssertionError("Expected event log response to contain a data list")
    actions = [event.get("action") for event in events["data"] if event.get("action") is not None]
    for expected in ["subject_created", "subject_updated"]:
        if expected not in actions:
            raise AssertionError(f"Expected event log to contain action {expected}")

    print("Deleting subject for user A...")
    delete_subject(token_a, subject_id)

    print("Verifying deleted subject is not accessible...")
    try:
        get_subject(token_a, subject_id)
        raise AssertionError("Deleted subject should not be retrievable")
    except requests.HTTPError as exc:
        if exc.response.status_code != 404:
            raise

    print("Attempting unauthorized deletion by user B...")
    try:
        delete_response = delete_subject(token_b, second_subject_id)
        if delete_response.status_code != 404:
            raise AssertionError("User B should not be able to delete user A's subject")
    except requests.HTTPError as exc:
        if exc.response.status_code != 404:
            raise

    print("Cleaning up second subject for user A...")
    delete_subject(token_a, second_subject_id)

    print("Validating unauthenticated access is rejected...")
    unauth_response = requests.get(f"{BASE_URL}/subjects")
    if unauth_response.status_code != 401:
        raise AssertionError("Unauthenticated access should return 401")

    print("All smoke tests passed.")


if __name__ == "__main__":
    run_smoke_tests()