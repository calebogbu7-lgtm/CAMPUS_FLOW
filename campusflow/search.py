"""Search utilities for CampusFlow ticket records."""

import re

VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")
VALID_STATUSES = ("open", "in_progress", "resolved")
VALID_PRIORITIES = ("critical", "high", "medium", "low")
PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def _normalise_text(value):
    """Normalise text for case-insensitive searches."""
    return re.sub(r"[^a-z0-9]", "", str(value).casefold())


def _normalise_filter(value, field_name, valid_values):
    """Return a canonical filter value or None when the filter is empty."""
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(f"{field_name} filter must be a string.")

    cleaned = value.strip()
    if not cleaned:
        return None

    lowered = cleaned.casefold()
    canonical = {item.casefold(): item for item in valid_values}

    if lowered not in canonical:
        raise ValueError(
            f"Invalid {field_name} filter: '{value}'. "
            f"Choose from: {', '.join(valid_values)}."
        )

    return canonical[lowered]


def search_tickets(
    tickets,
    title="",
    query="",
    category=None,
    status=None,
    priority=None,
):
    """Return tickets matching the supplied filters.

    Supports both the more explicit branch API (title=...) and the simpler
    repository API (query=...). Searches are case-insensitive and combine all
    supplied filters with AND logic.
    """
    if not isinstance(tickets, (list, tuple)):
        raise ValueError("Ticket data must be a list.")

    query_text = (title if title else query).strip()
    if not isinstance(query_text, str):
        raise ValueError("Search title must be text.")

    normalised_category = _normalise_filter(category, "category", VALID_CATEGORIES)
    normalised_status = _normalise_filter(status, "status", VALID_STATUSES)
    normalised_priority = _normalise_filter(priority, "priority", VALID_PRIORITIES)
    search_text = _normalise_text(query_text)

    matches = []
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a dictionary.")

        title_value = str(ticket.get("title", ""))
        if search_text and search_text not in _normalise_text(title_value):
            continue

        if normalised_category and ticket.get("category") != normalised_category:
            continue

        if normalised_status and ticket.get("status") != normalised_status:
            continue

        if normalised_priority and ticket.get("priority") != normalised_priority:
            continue

        matches.append(ticket)

    return matches


def sort_search_results(tickets):
    """Sort tickets by priority and then numeric ticket ID."""

    def sorting_key(ticket):
        priority = ticket["priority"]
        if not isinstance(priority, str):
            raise ValueError("Ticket priority must be text.")

        normalised_priority = priority.casefold()
        if normalised_priority not in PRIORITY_ORDER:
            raise ValueError(f"Invalid ticket priority: {priority}")

        ticket_id = ticket["ticket_id"]
        if not isinstance(ticket_id, str):
            raise ValueError("Ticket ID must be text.")

        if not ticket_id.startswith("T"):
            raise ValueError(f"Invalid ticket ID: {ticket_id}")

        suffix = ticket_id[1:]
        if not suffix.isdigit():
            raise ValueError(f"Invalid ticket ID: {ticket_id}")

        return PRIORITY_ORDER[normalised_priority], int(suffix)

    return sorted(tickets, key=sorting_key)

