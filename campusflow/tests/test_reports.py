"""Unit tests for CampusFlow reporting functionality."""

import unittest

from campusflow.reports import generate_report


def make_ticket(
    ticket_id="T001",
    status="open",
    priority="low",
    category="Network",
):
    """Create a ticket dictionary for report tests."""
    return {
        "ticket_id": ticket_id,
        "status": status,
        "priority": priority,
        "category": category,
    }


class TestReports(unittest.TestCase):
    """Tests for ticket statistics and report generation."""

    def test_generate_report(self):
        """Report totals and category, priority, and status counts."""
        tickets = [
            make_ticket(
                ticket_id="T001",
                status="open",
                priority="critical",
                category="Network",
            ),
            make_ticket(
                ticket_id="T002",
                status="in_progress",
                priority="high",
                category="Hardware",
            ),
            make_ticket(
                ticket_id="T003",
                status="resolved",
                priority="medium",
                category="Software",
            ),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total_tickets"], 3)

        self.assertEqual(
            report["by_status"],
            {
                "open": 1,
                "in_progress": 1,
                "resolved": 1,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 1,
                "high": 1,
                "medium": 1,
                "low": 0,
            },
        )

        self.assertEqual(
            report["by_category"],
            {
                "Network": 1,
                "Hardware": 1,
                "Software": 1,
                "Other": 0,
            },
        )

        self.assertEqual(report["unresolved_tickets"], 2)
        self.assertEqual(report["resolved_tickets"], 1)
        self.assertEqual(
            report["resolution_percentage"],
            33.33,
        )

    def test_empty_report(self):
        """An empty collection should produce zero counts and 0.0%."""
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

        self.assertEqual(
            report["by_category"],
            {
                "Network": 0,
                "Hardware": 0,
                "Software": 0,
                "Other": 0,
            },
        )

        self.assertEqual(report["unresolved_tickets"], 0)
        self.assertEqual(report["resolved_tickets"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_invalid_status(self):
        """An invalid ticket status should raise ValueError."""
        tickets = [
            make_ticket(status="pending"),
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_invalid_priority(self):
        """An invalid ticket priority should raise ValueError."""
        tickets = [
            make_ticket(priority="urgent"),
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_invalid_category(self):
        """An invalid ticket category should raise ValueError."""
        tickets = [
            make_ticket(category="Transport"),
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_missing_status_raises_key_error(self):
        """A ticket missing status should raise KeyError."""
        tickets = [
            {
                "ticket_id": "T001",
                "priority": "low",
                "category": "Network",
            }
        ]

        with self.assertRaises(KeyError):
            generate_report(tickets)

    def test_missing_priority_raises_key_error(self):
        """A ticket missing priority should raise KeyError."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "category": "Network",
            }
        ]

        with self.assertRaises(KeyError):
            generate_report(tickets)

    def test_missing_category_raises_key_error(self):
        """A ticket missing category should raise KeyError."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "priority": "low",
            }
        ]

        with self.assertRaises(KeyError):
            generate_report(tickets)

    def test_all_resolved_tickets_produce_100_percent(self):
        """A collection with all tickets resolved should report 100%."""
        tickets = [
            make_ticket(
                ticket_id="T001",
                status="resolved",
                priority="high",
            ),
            make_ticket(
                ticket_id="T002",
                status="resolved",
                priority="low",
                category="Hardware",
            ),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["resolved_tickets"], 2)
        self.assertEqual(report["unresolved_tickets"], 0)
        self.assertEqual(report["resolution_percentage"], 100.0)

    def test_unresolved_tickets_include_open_and_in_progress(self):
        """Open and in-progress tickets count as unresolved."""
        tickets = [
            make_ticket(
                ticket_id="T001",
                status="open",
            ),
            make_ticket(
                ticket_id="T002",
                status="in_progress",
            ),
            make_ticket(
                ticket_id="T003",
                status="resolved",
            ),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["unresolved_tickets"], 2)
        self.assertEqual(report["resolved_tickets"], 1)

    def test_resolution_percentage_is_rounded_to_two_decimal_places(self):
        """Resolution percentage should be rounded to two decimal places."""
        tickets = [
            make_ticket(
                ticket_id="T001",
                status="resolved",
            ),
            make_ticket(
                ticket_id="T002",
                status="open",
            ),
            make_ticket(
                ticket_id="T003",
                status="open",
            ),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["resolution_percentage"], 33.33)

    def test_current_status_determines_report_counts(self):
        """An open ticket counts as unresolved, not resolved."""
        tickets = [
            make_ticket(
                ticket_id="T001",
                status="open",
                priority="high",
            ),
            make_ticket(
                ticket_id="T002",
                status="resolved",
                priority="medium",
                category="Hardware",
            ),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["unresolved_tickets"], 1)
        self.assertEqual(report["resolved_tickets"], 1)
        self.assertEqual(report["resolution_percentage"], 50.0)


if __name__ == "__main__":
    unittest.main()