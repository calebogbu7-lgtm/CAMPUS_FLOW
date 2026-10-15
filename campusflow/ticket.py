"""Ticket validation, creation, and priority calculation."""

import re

VALID_URGENCIES = ("low", "medium", "high")
VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")

_next_ticket_number = 1


def validate_ticket_data(*args):
    """Support legacy two-argument and full four-argument validation."""

    if len(args) == 2:
        urgency, affected_users = args
        title = "Valid title"
        category = "Other"
    elif len(args) == 4:
        title, category, urgency, affected_users = args
    else:
        raise TypeError(
            "Expected (urgency, affected_users) or "
            "(title, category, urgency, affected_users)."
        )

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be blank.")

    if (
        not isinstance(category, str)
        or category.strip().casefold()
        not in {item.casefold() for item in VALID_CATEGORIES}
    ):
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )

    if (
        not isinstance(urgency, str)
        or urgency.strip().lower() not in VALID_URGENCIES
    ):
        raise ValueError("Urgency must be low, medium, or high.")

    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a whole number.")

    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return True


def calculate_priority(urgency, affected_users):
    """Calculate priority using the required rules."""

    validate_ticket_data(urgency, affected_users)
    urgency = urgency.strip().lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def generate_ticket_id(tickets=None):
    """Generate a sequential ticket ID without duplicating existing IDs."""

    global _next_ticket_number

    highest = _next_ticket_number - 1

    for ticket in tickets or []:
        ticket_id = ticket.get("ticket_id", "")

        if isinstance(ticket_id, str) and re.fullmatch(r"T\d{3,}", ticket_id):
            highest = max(highest, int(ticket_id[1:]))

    _next_ticket_number = highest + 2
    return f"T{highest + 1:03d}"


def sync_ticket_id(tickets):
    """Restore the ticket ID counter after loading saved tickets."""

    global _next_ticket_number

    highest = 0

    for ticket in tickets:
        ticket_id = ticket.get("ticket_id", "")

        if isinstance(ticket_id, str) and re.fullmatch(r"T\d{3,}", ticket_id):
            highest = max(highest, int(ticket_id[1:]))

    _next_ticket_number = highest + 1


def create_ticket(*args, tickets=None, **kwargs):
    """Create either a legacy-format or full CampusFlow ticket."""

    if kwargs:
        title = kwargs.pop("title", None)
        category = kwargs.pop("category", None)
        urgency = kwargs.pop("urgency", None)
        affected_users = kwargs.pop("affected_users", None)

        if kwargs:
            raise TypeError(f"Unexpected arguments: {', '.join(kwargs)}")

        if title is None and category is None:
            args = (urgency, affected_users)
        else:
            args = (title, category, urgency, affected_users)

    if len(args) == 2:
        urgency, affected_users = args
        title = None
        category = None
    elif len(args) == 4:
        title, category, urgency, affected_users = args
    else:
        raise TypeError(
            "Use create_ticket(urgency, affected_users) or "
            "create_ticket(title, category, urgency, affected_users)."
        )

    if title is None and category is None:
        validate_ticket_data(urgency, affected_users)
    else:
        validate_ticket_data(title, category, urgency, affected_users)

    urgency = urgency.strip().lower()

    ticket = {
        "ticket_id": generate_ticket_id(tickets),
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }

    if title is not None:
        ticket["title"] = title.strip()
        ticket["category"] = next(
            item for item in VALID_CATEGORIES
            if item.casefold() == category.strip().casefold()
        )
        ticket["notes"] = []

    return ticket
