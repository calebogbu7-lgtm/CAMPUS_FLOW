"""Unit tests for CampusFlow reporting functionality."""

import unittest

from campusflow.reports import generate_report


class TestReports(unittest.TestCase):
    """Tests for ticket statistics and report generation."""

    def test_generate_report(self):
        """Report totals, status, priority, and category counts."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "priority": "critical",
                "category": "Network",
            },
            {
                "ticket_id": "T002",
                "status": "in_progress",
                "priority": "high",
                "category": "Hardware",
            },
            {
                "ticket_id": "T003",
                "status": "resolved",
                "priority": "medium",
                "category": "Software",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total_tickets"], 3)

        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)

        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["medium"], 1)
        self.assertEqual(report["by_priority"]["low"], 0)

        self.assertEqual(report["by_category"]["Network"], 1)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["by_category"]["Software"], 1)
        self.assertEqual(report["by_category"]["Other"], 0)

        self.assertEqual(report["unresolved_tickets"], 2)
        self.assertEqual(report["resolved_tickets"], 1)
        self.assertEqual(report["resolution_percentage"], 33.33)

    def test_empty_report(self):
        """An empty collection should produce zero counts and zero percent."""
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_status"]["in_progress"], 0)
        self.assertEqual(report["by_status"]["resolved"], 0)

        self.assertEqual(report["by_priority"]["critical"], 0)
        self.assertEqual(report["by_category"]["Network"], 0)

        self.assertEqual(report["unresolved_tickets"], 0)
        self.assertEqual(report["resolved_tickets"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_invalid_status(self):
        """An invalid ticket status should raise ValueError."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "pending",
                "priority": "low",
                "category": "Network",
            }
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_invalid_priority(self):
        """An invalid ticket priority should raise ValueError."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "priority": "urgent",
                "category": "Network",
            }
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_invalid_category(self):
        """An invalid ticket category should raise ValueError."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "priority": "low",
                "category": "Transport",
            }
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_reopened_ticket_counts_by_current_status(self):
        """A reopened ticket counts as open, not resolved."""
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "priority": "high",
                "category": "Network",
            },
            {
                "ticket_id": "T002",
                "status": "resolved",
                "priority": "medium",
                "category": "Hardware",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["unresolved_tickets"], 1)
        self.assertEqual(report["resolved_tickets"], 1)
        self.assertEqual(report["resolution_percentage"], 50.0)


if __name__ == "__main__":
    unittest.main()