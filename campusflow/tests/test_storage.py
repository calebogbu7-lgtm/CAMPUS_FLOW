import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets
from campusflow.ticket import create_ticket

def sample_ticket(ticket_id="T001"):
    return {
        "ticket_id": ticket_id,
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": "open",
        "assigned_to": None,
    }


class TestStorage(unittest.TestCase):

    def test_save_and_load_tickets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = [sample_ticket()]

            save_tickets(tickets, path)

            self.assertEqual(load_tickets(path), tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"
            self.assertEqual(load_tickets(path), [])

    def test_invalid_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{invalid", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_json_must_contain_a_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps({"ticket_id": "T001"}), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_invalid_ticket_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([{"ticket_id": "T001"}]), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_duplicate_ticket_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(
                json.dumps([sample_ticket(), sample_ticket()]),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_ticket_id_continues_after_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets([sample_ticket("T014")], path)

            load_tickets(path)
            new_ticket = create_ticket("low", 1)

            self.assertEqual(new_ticket["ticket_id"], "T015")

    def test_invalid_ticket_cannot_be_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            with self.assertRaises(ValueError):
                save_tickets([{"ticket_id": "T001"}], path)

            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
