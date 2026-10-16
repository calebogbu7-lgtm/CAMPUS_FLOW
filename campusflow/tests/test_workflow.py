import unittest

from campusflow.workflow import (
    assign_ticket,
    get_work_queue,
    update_status,
)


def make_ticket(ticket_id="T001", priority="high", status="open"):
    """Create a simple ticket fixture for workflow tests."""
    return {
        "ticket_id": ticket_id,
        "urgency": "high",
        "affected_users": 5,
        "priority": priority,
        "status": status,
        "assigned_to": None,
    }


class TestWorkflow(unittest.TestCase):
    """Test ticket assignment, status transitions, and work queues."""

    def test_assign_ticket(self):
        ticket = make_ticket()

        assign_ticket(ticket, " Caleb ")

        self.assertEqual(ticket["assigned_to"], "Caleb")

    def test_empty_staff_name_is_rejected(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            assign_ticket(ticket, "   ")

        self.assertIsNone(ticket["assigned_to"])

    def test_resolved_ticket_cannot_be_assigned(self):
        ticket = make_ticket(status="resolved")

        with self.assertRaises(ValueError):
            assign_ticket(ticket, "Caleb")

        self.assertIsNone(ticket["assigned_to"])

    def test_ticket_must_be_assigned_before_work(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            update_status(ticket, "in_progress")

        self.assertEqual(ticket["status"], "open")

    def test_valid_status_transitions(self):
        ticket = make_ticket()

        assign_ticket(ticket, "Caleb")

        update_status(ticket, "in_progress")
        self.assertEqual(ticket["status"], "in_progress")

        update_status(ticket, "resolved")
        self.assertEqual(ticket["status"], "resolved")

    def test_invalid_status_transition(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            update_status(ticket, "resolved")

        self.assertEqual(ticket["status"], "open")

    def test_invalid_status_name(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            update_status(ticket, "pending")

        self.assertEqual(ticket["status"], "open")

    def test_resolved_tickets_are_excluded_from_queue(self):
        open_ticket = make_ticket("T001", "high", "open")
        resolved_ticket = make_ticket("T002", "critical", "resolved")

        queue = get_work_queue([open_ticket, resolved_ticket])

        self.assertEqual(
            [ticket["ticket_id"] for ticket in queue],
            ["T001"],
        )

    def test_in_progress_tickets_are_excluded_from_queue(self):
        open_ticket = make_ticket("T001", "high", "open")
        in_progress_ticket = make_ticket(
            "T002",
            "critical",
            "in_progress",
        )

        queue = get_work_queue([open_ticket, in_progress_ticket])

        self.assertEqual(
            [ticket["ticket_id"] for ticket in queue],
            ["T001"],
        )

    def test_queue_prioritizes_critical_tickets(self):
        low_ticket = make_ticket("T001", "low")
        critical_ticket = make_ticket("T002", "critical")
        high_ticket = make_ticket("T003", "high")

        queue = get_work_queue(
            [low_ticket, critical_ticket, high_ticket]
        )

        self.assertEqual(
            [ticket["priority"] for ticket in queue],
            ["critical", "high", "low"],
        )

    def test_queue_uses_numeric_ticket_id_for_priority_ties(self):
        ticket_10 = make_ticket("T010", "high")
        ticket_2 = make_ticket("T002", "high")
        ticket_1 = make_ticket("T001", "high")

        queue = get_work_queue(
            [ticket_10, ticket_2, ticket_1]
        )

        self.assertEqual(
            [ticket["ticket_id"] for ticket in queue],
            ["T001", "T002", "T010"],
        )

    def test_queue_rejects_invalid_priority(self):
        ticket = make_ticket(priority="urgent")

        with self.assertRaises(ValueError):
            get_work_queue([ticket])

    def test_queue_rejects_missing_ticket_id(self):
        ticket = make_ticket()
        ticket["ticket_id"] = None

        with self.assertRaises(ValueError):
            get_work_queue([ticket])

    def test_queue_rejects_invalid_ticket_status(self):
        ticket = make_ticket(status="pending")

        with self.assertRaises(ValueError):
            get_work_queue([ticket])

    def test_queue_rejects_non_list_input(self):
        with self.assertRaises(ValueError):
            get_work_queue("not a ticket list")

    def test_queue_accepts_empty_collection(self):
        self.assertEqual(get_work_queue([]), [])

    def test_queue_does_not_modify_input_order(self):
        low_ticket = make_ticket("T001", "low")
        critical_ticket = make_ticket("T002", "critical")
        tickets = [low_ticket, critical_ticket]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["ticket_id"] for ticket in tickets],
            ["T001", "T002"],
        )

        self.assertEqual(
            [ticket["ticket_id"] for ticket in queue],
            ["T002", "T001"],
        )


if __name__ == "__main__":
    unittest.main()