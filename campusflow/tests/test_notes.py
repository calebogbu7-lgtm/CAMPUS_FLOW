import unittest

from campusflow.notes import add_note, get_ticket_notes


def make_ticket(status="open"):
    return {
        "ticket_id": "T001",
        "status": status,
        "notes": [],
    }


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = [make_ticket()]

    def test_add_note_successfully(self):
        note = add_note(
            self.tickets, "T001", "Caleb", "The issue is being investigated."
        )
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Caleb")
        self.assertEqual(len(self.tickets[0]["notes"]), 1)

    def test_note_fields_are_trimmed(self):
        note = add_note(
            self.tickets, "T001", " Caleb ", "  Checking the network now.  "
        )
        self.assertEqual(note["author"], "Caleb")
        self.assertEqual(note["message"], "Checking the network now.")

    def test_blank_author_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "  ", "A valid note message.")
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_short_message_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Caleb", "Bad")
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_missing_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Caleb", "A valid note message.")

    def test_resolved_ticket_rejects_note(self):
        self.tickets[0]["status"] = "resolved"
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Caleb", "A valid note message.")
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_note_ids_increment(self):
        add_note(self.tickets, "T001", "Caleb", "First update message.")
        second = add_note(
            self.tickets, "T001", "Ada", "Second update message."
        )
        self.assertEqual(second["note_id"], "N002")

    def test_get_ticket_notes(self):
        add_note(self.tickets, "T001", "Caleb", "First update message.")
        add_note(self.tickets, "T001", "Ada", "Second update message.")
        notes = get_ticket_notes(self.tickets, "T001")
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0]["note_id"], "N001")
        self.assertEqual(notes[1]["note_id"], "N002")


if __name__ == "__main__":
    unittest.main()
