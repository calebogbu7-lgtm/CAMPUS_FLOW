"""Unit tests for CampusFlow ticket search functionality."""

import unittest

from campusflow.search import search_tickets, sort_search_results


class TestSearchTickets(unittest.TestCase):
    """Tests for searching tickets using titles and filters."""

    def test_title_search_is_case_insensitive(self):
        """Title search should match regardless of letter case."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "WiFi connection failure",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            }
        ]

        results = search_tickets(tickets, title="wifi")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T001")

    def test_title_search_matches_partial_text(self):
        """Title search should match a substring of the title."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "Internet connection failure",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

        results = search_tickets(tickets, title="connection")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T001")

    def test_search_returns_no_results_for_nonmatching_title(self):
        """A title that does not match should return an empty list."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "Broken projector",
                "category": "Hardware",
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
            }
        ]

        results = search_tickets(tickets, title="internet")

        self.assertEqual(results, [])

    def test_combined_filters_use_and_logic(self):
        """All supplied filters must match the same ticket."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "Internet outage affecting students",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
            {
                "ticket_id": "T002",
                "title": "Internet connection is slow",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": "Samuel",
            },
            {
                "ticket_id": "T003",
                "title": "Broken projector",
                "category": "Hardware",
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
        ]

        results = search_tickets(
            tickets,
            title="internet",
            category="Network",
            status="open",
            priority="critical",
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T001")

    def test_search_filters_are_case_insensitive(self):
        """Category, status, priority and title matching ignore case."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "WiFi connection failure",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            }
        ]

        results = search_tickets(
            tickets,
            title="WIFI",
            category="network",
            status="OPEN",
            priority="HIGH",
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ticket_id"], "T001")

    def test_sort_search_results_by_priority_and_ticket_id(self):
        """Search results should sort by priority, then numeric ticket ID."""
        tickets = [
            {
                "ticket_id": "T010",
                "title": "Network issue ten",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            },
            {
                "ticket_id": "T002",
                "title": "Network issue two",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
            {
                "ticket_id": "T001",
                "title": "Network issue one",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            },
            {
                "ticket_id": "T003",
                "title": "Network issue three",
                "category": "Network",
                "priority": "low",
                "status": "open",
                "assigned_to": None,
            },
        ]

        results = sort_search_results(tickets)

        self.assertEqual(
            [ticket["ticket_id"] for ticket in results],
            ["T002", "T001", "T010", "T003"],
        )

    def test_empty_optional_filters_do_not_restrict_results(self):
        """Empty optional filters should not exclude any tickets."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "Broken projector",
                "category": "Hardware",
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
            },
            {
                "ticket_id": "T002",
                "title": "WiFi failure",
                "category": "Network",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "Samuel",
            },
        ]

        results = search_tickets(
            tickets,
            category="",
            status="",
            priority="",
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(
            [ticket["ticket_id"] for ticket in results],
            ["T001", "T002"],
        )

    def test_search_does_not_modify_original_tickets(self):
        """Searching should not change the original ticket collection."""
        tickets = [
            {
                "ticket_id": "T001",
                "title": "Broken projector",
                "category": "Hardware",
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
            }
        ]

        original_tickets = [ticket.copy() for ticket in tickets]

        search_tickets(tickets, title="projector")

        self.assertEqual(tickets, original_tickets)


if __name__ == "__main__":
    unittest.main()
