"""Tests for CampusFlow ticket searching and sorting."""

import unittest

from campusflow.search import search_tickets, sort_search_results


def make_ticket(
    ticket_id="T001",
    title="Broken projector",
    category="Hardware",
    priority="medium",
    status="open",
    assigned_to=None,
):
    return {
        "ticket_id": ticket_id,
        "title": title,
        "category": category,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestSearchTickets(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket(
                ticket_id="T010",
                title="WiFi connection failure",
                category="Network",
                priority="high",
                status="open",
                assigned_to="Samuel",
            ),
            make_ticket(
                ticket_id="T002",
                title="Broken projector",
                category="Hardware",
                priority="medium",
                status="in_progress",
                assigned_to="Mary",
            ),
            make_ticket(
                ticket_id="T003",
                title="Software installation issue",
                category="Software",
                priority="critical",
                status="open",
                assigned_to=None,
            ),
            make_ticket(
                ticket_id="T004",
                title="WiFi router overheating",
                category="Network",
                priority="low",
                status="resolved",
                assigned_to="Faith",
            ),
        ]

    def test_title_search_is_case_insensitive(self):
        results = search_tickets(self.tickets, title="WIFI")
        self.assertEqual([ticket["ticket_id"] for ticket in results], ["T010", "T004"])

    def test_partial_title_search(self):
        results = search_tickets(self.tickets, title="project")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T002")

    def test_combined_filters_use_and_logic(self):
        results = search_tickets(
            self.tickets,
            title="wifi",
            category="Network",
            status="open",
            priority="high",
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T010")

    def test_filters_are_case_insensitive(self):
        results = search_tickets(
            self.tickets,
            title="SOFTWARE",
            category="software",
            status="OPEN",
            priority="CRITICAL",
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T003")

    def test_empty_optional_filters_do_not_restrict_results(self):
        results = search_tickets(self.tickets, category="", status="   ", priority="")
        self.assertEqual(len(results), len(self.tickets))

    def test_invalid_category_filter_raises_value_error(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="Transport")

    def test_invalid_status_filter_raises_value_error(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status="pending")

    def test_invalid_priority_filter_raises_value_error(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, priority="urgent")

    def test_sort_search_results_orders_by_priority_and_ticket_number(self):
        tickets = [
            {"ticket_id": "T010", "priority": "high"},
            {"ticket_id": "T002", "priority": "high"},
            {"ticket_id": "T001", "priority": "high"},
        ]
        self.assertEqual(
            [ticket["ticket_id"] for ticket in sort_search_results(tickets)],
            ["T001", "T002", "T010"],
        )


class TestSearchLegacyCompatibility(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

    def test_non_string_filter_raises_value_error(self):
        """A non-string filter should be rejected."""
        with self.assertRaises(ValueError):
            search_tickets(
                self.tickets,
                category=123,
            )

    def test_non_string_title_raises_value_error(self):
        """A non-string title should be rejected."""
        with self.assertRaises(ValueError):
            search_tickets(
                self.tickets,
                title=None,
            )

    def test_search_empty_collection_returns_empty_list(self):
        """Searching an empty collection returns an empty list."""
        self.assertEqual(search_tickets([]), [])

    def test_search_does_not_modify_original_collection(self):
        """Searching should preserve the original list and its tickets."""
        original_list = list(self.tickets)
        original_ticket_values = [
            ticket.copy() for ticket in self.tickets
        ]

        search_tickets(
            self.tickets,
            title="wifi",
            category="Network",
        )

        self.assertEqual(self.tickets, original_list)
        self.assertEqual(
            self.tickets,
            original_ticket_values,
        )


class TestSortSearchResults(unittest.TestCase):
    """Tests for priority and ticket-ID sorting."""

    def test_sort_uses_priority_then_numeric_ticket_id(self):
        """Higher priorities come first, with numeric IDs as tie-breakers."""
        tickets = [
            make_ticket(
                ticket_id="T010",
                priority="high",
            ),
            make_ticket(
                ticket_id="T002",
                priority="critical",
            ),
            make_ticket(
                ticket_id="T003",
                priority="high",
            ),
            make_ticket(
                ticket_id="T001",
                priority="low",
            ),
            make_ticket(
                ticket_id="T004",
                priority="medium",
            ),
        ]

        results = sort_search_results(tickets)

        self.assertEqual(
            [ticket["ticket_id"] for ticket in results],
            ["T002", "T003", "T010", "T004", "T001"],
        )

    def test_sort_does_not_modify_original_list(self):
        """Sorting returns a new list and preserves original order."""
        tickets = [
            make_ticket(ticket_id="T010", priority="low"),
            make_ticket(ticket_id="T002", priority="critical"),
        ]
        original_order = list(tickets)

        results = sort_search_results(tickets)

        self.assertEqual(tickets, original_order)
        self.assertIsNot(results, tickets)

    def test_sort_rejects_invalid_priority(self):
        """An invalid priority should raise ValueError."""
        tickets = [
            make_ticket(
                ticket_id="T001",
                priority="urgent",
            )
        ]

        with self.assertRaises(ValueError):
            sort_search_results(tickets)

    def test_sort_rejects_invalid_ticket_id(self):
        """A ticket ID without a numeric suffix should be rejected."""
        tickets = [
            make_ticket(
                ticket_id="TABC",
                priority="high",
            )
        ]

        with self.assertRaises(ValueError):
            sort_search_results(tickets)


if __name__ == "__main__":
    unittest.main()
