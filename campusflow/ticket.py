_next_ticket_number = 1

VALID_URGENCIES = ("low", "medium", "high")
VALID_CATEGORIES = ("network", "hardware", "software", "other")


def generate_ticket_id():
    """Generate a unique ticket ID."""

    global _next_ticket_number

    ticket_id = f"T{_next_ticket_number:03d}"
    _next_ticket_number += 1

    return ticket_id


def validate_ticket_data(title, category, urgency, affected_users):
    """Validate all ticket details."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be blank.")

    if (
        not isinstance(category, str)
        or category.strip().lower() not in VALID_CATEGORIES
    ):
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )

    if (
        not isinstance(urgency, str)
        or urgency.strip().lower() not in VALID_URGENCIES
    ):
        raise ValueError("Urgency must be low, medium, or high.")

    if (
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
    ):
        raise ValueError("Affected users must be a whole number.")

    if affected_users < 1:
        raise ValueError("At least one user must be affected.")

    return True



def calculate_priority(urgency, affected_users):
    """Calculate priority using the required rules."""

    if (
        not isinstance(urgency, str)
        or urgency.strip().lower() not in VALID_URGENCIES
    ):
        raise ValueError("Urgency must be low, medium, or high.")

    if (
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
        or affected_users < 1
    ):
        raise ValueError("Affected users must be a positive whole number.")

    urgency = urgency.strip().lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"



def create_ticket(title, category, urgency, affected_users):
    """Validate details and create a ticket."""

    validate_ticket_data(
        title,
        category,
        urgency,
        affected_users,
    )

    title = title.strip()
    category = category.strip().title()
    urgency = urgency.strip().lower()

    priority = calculate_priority(urgency, affected_users)

    ticket = {
        "ticket_id": generate_ticket_id(),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    return ticket