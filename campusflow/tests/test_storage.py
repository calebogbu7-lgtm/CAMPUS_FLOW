import json
import tempfile
import unittest
from pathlib import Path

from storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):

    def test_save_and_load_tickets(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tickets.json"

            tickets = [
                {
                    "ticket_id": "T001",
                    "urgency": "high",
                    "affected_users": 12,
                    "priority": "critical",
                    "status": "open",
                    "assigned_to": None,
                }
            ]

            save_tickets(tickets, file_path)
            loaded = load_tickets(file_path)

            self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "missing.json"

            self.assertEqual(load_tickets(file_path), [])

    def test_invalid_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tickets.json"
            file_path.write_text("{invalid", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(file_path)

    def test_json_must_contain_a_list(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tickets.json"
            file_path.write_text(
                json.dumps({"ticket_id": "T001"}),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(file_path)


if __name__ == "__main__":
    unittest.main()
