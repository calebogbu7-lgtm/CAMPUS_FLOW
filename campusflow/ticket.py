_next_ticket_number = 1


def generate_ticket_id():
    global _next_ticket_number

    ticket_id = f"T{_next_ticket_number:03d}"
    _next_ticket_number += 1

    return ticket_id


def validate_ticket_data(urgency, affected_users):
    valid_urgencies = ("low", "medium", "high")

    if urgency not in valid_urgencies:
        raise ValueError(
            "Urgency must be low, medium, or high."
        )

    if (
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
    ):
        raise ValueError(
            "Affected users must be a whole number."
        )

    if affected_users < 1:
        raise ValueError(
            "At least one user must be affected."
        )

    return True


def calculate_priority(urgency, affected_users):
    validate_ticket_data(urgency, affected_users)

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def create_ticket(urgency, affected_users):
    priority = calculate_priority(urgency, affected_users)

    ticket = {
        "ticket_id": generate_ticket_id(),
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    return ticket

