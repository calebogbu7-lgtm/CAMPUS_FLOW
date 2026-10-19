def assign_ticket(ticket, staff_name):
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("A valid staff name is required.")

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def update_status(ticket, new_status):
    allowed_transitions = {
        "open": ["in_progress"],
        "in_progress": ["resolved"],
        "resolved": ["open"],  # changed: lets a resolved ticket be reopened
    }

    if new_status not in ("open", "in_progress", "resolved"):
        raise ValueError("Invalid ticket status.")

    current_status = ticket.get("status")

    if current_status not in allowed_transitions:
        raise ValueError("The ticket has an invalid current status.")

    if new_status not in allowed_transitions[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} "
            f"to {new_status}."
        )

    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Assign the ticket before starting work.")

    ticket["status"] = new_status

    return ticket


def get_work_queue(tickets):
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket.get("status") != "resolved"
    ]

    for ticket in unresolved_tickets:
        if ticket.get("priority") not in priority_order:
            raise ValueError("A ticket has an invalid priority.")

    unresolved_tickets.sort(
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            ticket["ticket_id"],
        )
    )

    return unresolved_tickets