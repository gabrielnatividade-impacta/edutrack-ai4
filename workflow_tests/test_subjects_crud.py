import os
import time
import unittest
import requests

BASE_URL = os.getenv("XANO_BASE_URL", "").rstrip("/")
AUTH_TOKEN = os.getenv("XANO_AUTH_TOKEN")
OTHER_AUTH_TOKEN = os.getenv("XANO_OTHER_AUTH_TOKEN")


def auth_headers(token=None):
    token = token or AUTH_TOKEN
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def wait_for_event(action, subject_id, timeout=10):
    if not BASE_URL or not AUTH_TOKEN:
        return None

    url = f"{BASE_URL}/logs/user/my_events"
    end_time = time.time() + timeout
    while time.time() < end_time:
        response = requests.get(url, headers=auth_headers())
        if response.status_code == 200:
            for event in response.json():
                if event.get("action") == action and event.get("metadata", {}).get("subject_id") == subject_id:
                    return event
        time.sleep(1)
    return None


class SubjectCrudTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BASE_URL or not AUTH_TOKEN:
            raise unittest.SkipTest("XANO_BASE_URL and XANO_AUTH_TOKEN are required to run subject API tests")

    def create_subject(self, payload):
        url = f"{BASE_URL}/subjects"
        return requests.post(url, json=payload, headers=auth_headers())

    def test_01_create_subject_valid(self):
        payload = {"name": "Test Subject", "code": "TEST101", "semester": "Spring", "description": "Unit test subject"}
        response = self.create_subject(payload)
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result["name"], payload["name"])
        self.assertEqual(result["code"], payload["code"])
        self.assertIn("user_id", result)
        self.assertIn("created_at", result)
        self.assertIn("updated_at", result)
        self.assertEqual(result["created_at"], result["updated_at"])
        self.created_subject_id = result["id"]

    def test_02_create_subject_missing_required(self):
        response = self.create_subject({"name": "", "code": ""})
        self.assertEqual(response.status_code, 400)

    def test_03_list_subjects_for_user(self):
        url = f"{BASE_URL}/subjects?limit=10&offset=0"
        response = requests.get(url, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertIn("count", data)
        self.assertIn("offset", data)
        self.assertIn("limit", data)

    def test_04_get_subject_by_id(self):
        create_resp = self.create_subject({"name": "Detail Subject", "code": "DETAIL101"})
        self.assertEqual(create_resp.status_code, 201)
        subject_id = create_resp.json()["id"]

        url = f"{BASE_URL}/subjects/{subject_id}"
        response = requests.get(url, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["id"], subject_id)

    def test_05_update_subject_owned(self):
        create_resp = self.create_subject({"name": "Update Subject", "code": "UPDATE101"})
        self.assertEqual(create_resp.status_code, 201)
        subject_id = create_resp.json()["id"]

        url = f"{BASE_URL}/subjects/{subject_id}"
        response = requests.put(url, json={"name": "Updated Name", "semester": "Fall"}, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["name"], "Updated Name")
        self.assertEqual(result["semester"], "Fall")

    def test_06_update_subject_unowned_or_not_found(self):
        target_id = 99999999
        if OTHER_AUTH_TOKEN:
            response = requests.put(f"{BASE_URL}/subjects/{target_id}", json={"name": "No Access"}, headers=auth_headers(OTHER_AUTH_TOKEN))
        else:
            response = requests.put(f"{BASE_URL}/subjects/{target_id}", json={"name": "No Access"}, headers=auth_headers())
        self.assertEqual(response.status_code, 404)

    def test_07_delete_subject_owned(self):
        create_resp = self.create_subject({"name": "Delete Subject", "code": "DELETE101"})
        self.assertEqual(create_resp.status_code, 201)
        subject_id = create_resp.json()["id"]

        response = requests.delete(f"{BASE_URL}/subjects/{subject_id}", headers=auth_headers())
        self.assertEqual(response.status_code, 204)

    def test_08_delete_subject_unowned_or_not_found(self):
        target_id = 99999998
        if OTHER_AUTH_TOKEN:
            response = requests.delete(f"{BASE_URL}/subjects/{target_id}", headers=auth_headers(OTHER_AUTH_TOKEN))
        else:
            response = requests.delete(f"{BASE_URL}/subjects/{target_id}", headers=auth_headers())
        self.assertEqual(response.status_code, 404)

    def test_09_unauthenticated_access(self):
        response = requests.get(f"{BASE_URL}/subjects")
        self.assertEqual(response.status_code, 401)

    def test_10_user_id_immutable_on_put(self):
        create_resp = self.create_subject({"name": "Immutable Test", "code": "IMMUTABLE101"})
        self.assertEqual(create_resp.status_code, 201)
        subject = create_resp.json()
        subject_id = subject["id"]

        response = requests.put(
            f"{BASE_URL}/subjects/{subject_id}",
            json={"name": "Immutable Updated", "user_id": 9999999},
            headers=auth_headers(),
        )
        self.assertIn(response.status_code, (200, 400))
        if response.status_code == 200:
            updated = response.json()
            self.assertEqual(updated["user_id"], subject["user_id"])

    def test_11_edge_case_validation(self):
        response = self.create_subject({"name": "", "code": ""})
        self.assertEqual(response.status_code, 400)

        long_code = "X" * 25
        response = self.create_subject({"name": "Long Code", "code": long_code})
        self.assertEqual(response.status_code, 400)

    def test_12_event_logging_on_actions(self):
        create_resp = self.create_subject({"name": "Event Subject", "code": "EVENT101"})
        self.assertEqual(create_resp.status_code, 201)
        subject_id = create_resp.json()["id"]

        # If event logging is not processed immediately, fetch it with retries.
        create_event = wait_for_event("subject_created", subject_id)
        self.assertIsNotNone(create_event)

        update_resp = requests.put(
            f"{BASE_URL}/subjects/{subject_id}",
            json={"name": "Event Updated"},
            headers=auth_headers(),
        )
        self.assertEqual(update_resp.status_code, 200)
        update_event = wait_for_event("subject_updated", subject_id)
        self.assertIsNotNone(update_event)

        delete_resp = requests.delete(f"{BASE_URL}/subjects/{subject_id}", headers=auth_headers())
        self.assertEqual(delete_resp.status_code, 204)
        delete_event = wait_for_event("subject_deleted", subject_id)
        self.assertIsNotNone(delete_event)

        if OTHER_AUTH_TOKEN:
            other_response = requests.get(f"{BASE_URL}/subjects/{subject_id}", headers=auth_headers(OTHER_AUTH_TOKEN))
            self.assertEqual(other_response.status_code, 404)
            denied_event = wait_for_event("subject_access_denied", subject_id)
            self.assertIsNotNone(denied_event)


if __name__ == "__main__":
    unittest.main()
