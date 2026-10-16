"""Search utilities for CampusFlow ticket records."""

import re

VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")
VALID_STATUSES = ("open", "in_progress", "resolved")
VALID_PRIORITIES = ("critical", "high", "medium", "low")


def _normalise_text(value):
    """Lowercase and strip punctuation so search behaves consistently."""
    return re.sub(r"[^a-z0-9]", "", str(value).casefold())


def _normalise_filter(value, field_name, valid_values):
    """Normalise search filters and reject invalid values."""
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(f"{field_name} filter must be a string.")

    cleaned = value.strip()
    if not cleaned:
        return None

    lowered = cleaned.casefold()
    canonical = {
        item.casefold(): item for item in valid_values
    }

    if lowered not in canonical:
        raise ValueError(
            f"Invalid {field_name} filter: '{value}'. "
            f"Choose from: {', '.join(valid_values)}."
        )

    return canonical[lowered]


def search_tickets(tickets, query="", category=None, status=None, priority=None):
    """Return tickets matching title text and any supplied filters.

    Empty filter values mean "do not filter". Search is read-only and
    does not mutate the original collection.
    """
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a list.")

    normalised_category = _normalise_filter(category, "category", VALID_CATEGORIES)
    normalised_status = _normalise_filter(status, "status", VALID_STATUSES)
    normalised_priority = _normalise_filter(priority, "priority", VALID_PRIORITIES)

    search_text = ""
    if isinstance(query, str):
        search_text = _normalise_text(query.strip())

    matches = []
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a dictionary.")

        title = str(ticket.get("title", ""))
        if search_text and search_text not in _normalise_text(title):
            continue

        if normalised_category and ticket.get("category") != normalised_category:
            continue

        if normalised_status and ticket.get("status") != normalised_status:
            continue

        if normalised_priority and ticket.get("priority") != normalised_priority:
            continue

        matches.append(ticket)

    return matches
