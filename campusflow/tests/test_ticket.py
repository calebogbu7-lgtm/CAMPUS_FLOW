import unittest

from campusflow.ticket import (
    calculate_priority,
    create_ticket,
    validate_ticket_data,
)

class TestTicketCreation(unittest.TestCase):

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_priority(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("medium", 3), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 5)

    def test_zero_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("low", 0)

    def test_fractional_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("medium", 2.5)

    def test_boolean_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("low", True)

    def test_ticket_structure(self):
        ticket = create_ticket("high", 12)

        self.assertEqual(len(ticket["ticket_id"]), 4)
        self.assertTrue(ticket["ticket_id"].startswith("T"))
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_ticket_ids_are_unique(self):
        first = create_ticket("low", 1)
        second = create_ticket("low", 1)

        self.assertNotEqual(first["ticket_id"], second["ticket_id"])


if __name__ == "__main__":
    unittest.main()
