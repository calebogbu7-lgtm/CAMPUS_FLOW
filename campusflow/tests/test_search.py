import unittest

from campusflow.reports import generate_report
from campusflow.search import search_tickets


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "ticket_id": "T001",
                "title": "Wi-Fi outage in Lab 1",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": "Ada",
                "notes": [],
            },
            {
                "ticket_id": "T002",
                "title": "Laptop battery issue",
                "category": "Hardware",
                "urgency": "medium",
                "affected_users": 4,
                "priority": "medium",
                "status": "in_progress",
                "assigned_to": "Lin",
                "notes": [],
            },
            {
                "ticket_id": "T003",
                "title": "Office 365 login trouble",
                "category": "Software",
                "urgency": "low",
                "affected_users": 2,
                "priority": "low",
                "status": "resolved",
                "assigned_to": "Sam",
                "notes": [],
            },
            {
                "ticket_id": "T004",
                "title": "Wi-Fi outage in Lab 2",
                "category": "Network",
                "urgency": "high",
                "affected_users": 8,
                "priority": "high",
                "status": "open",
                "assigned_to": None,
                "notes": [],
            },
        ]

    def test_search_title_ignores_case(self):
        matches = search_tickets(self.tickets, query="wi-fi")
        self.assertEqual([ticket["ticket_id"] for ticket in matches], ["T001", "T004"])

    def test_combined_filters_use_and_logic(self):
        matches = search_tickets(
            self.tickets,
            query="wifi",
            category="Network",
            status="open",
            priority="high",
        )
        self.assertEqual([ticket["ticket_id"] for ticket in matches], ["T004"])

    def test_empty_filters_do_not_filter(self):
        matches = search_tickets(self.tickets, query="", category="", status="", priority="")
        self.assertEqual(len(matches), 4)

    def test_invalid_filter_value_raises(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="Unknown")


class TestReportInsights(unittest.TestCase):

    def test_report_tracks_category_and_resolution(self):
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
                "category": "Network",
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
        self.assertEqual(report["by_category"]["Network"], 2)
        self.assertEqual(report["unresolved_count"], 2)
        self.assertEqual(report["resolved_count"], 1)
        self.assertAlmostEqual(report["resolution_percentage"], 33.33, places=2)

    def test_empty_report_has_zero_resolution(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["resolved_count"], 0)
        self.assertEqual(report["resolution_percentage"], 0)


if __name__ == "__main__":
    unittest.main()
