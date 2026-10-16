"""Manage ticket assignments, status transitions, and work queues."""

VALID_STATUSES = {"open", "in_progress", "resolved"}

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": set(),
}


def _validate_ticket(ticket):
    """Validate the basic structure required by workflow operations."""
    if not isinstance(ticket, dict):
        raise ValueError("Ticket must be a dictionary.")

    status = ticket.get("status")

    if status not in VALID_STATUSES:
        raise ValueError("The ticket has an invalid status.")


def assign_ticket(ticket, staff_name):
    """Assign an eligible ticket to a staff member.

    Resolved tickets cannot be assigned or reassigned unless they
    are reopened through the valid workflow.
    """
    _validate_ticket(ticket)

    if ticket["status"] == "resolved":
        raise ValueError(
            "A resolved ticket cannot be assigned. Reopen it first."
        )

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("A valid staff name is required.")

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def update_status(ticket, new_status):
    """Update a ticket status when the transition is permitted.

    Valid lifecycle:
        open -> in_progress -> resolved

    A ticket must have an assignee before entering in_progress.
    """
    _validate_ticket(ticket)

    if not isinstance(new_status, str):
        raise ValueError("Invalid ticket status.")

    new_status = new_status.strip().casefold()

    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid ticket status.")

    current_status = ticket["status"]

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} "
            f"to {new_status}."
        )

    if new_status == "in_progress":
        assigned_to = ticket.get("assigned_to")

        if not isinstance(assigned_to, str) or not assigned_to.strip():
            raise ValueError("Assign the ticket before starting work.")

    ticket["status"] = new_status

    return ticket


def _ticket_id_sort_key(ticket_id):
    """Return a deterministic sort key for CampusFlow ticket IDs.

    Numeric IDs such as T002 and T010 are ordered numerically so
    that T002 correctly comes before T010.
    """
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("A ticket has an invalid ticket ID.")

    ticket_id = ticket_id.strip()

    if ticket_id.startswith("T"):
        suffix = ticket_id[1:]

        if suffix.isdigit():
            return (0, int(suffix))

    return (1, ticket_id.casefold())


def get_work_queue(tickets):
    """Return only OPEN tickets sorted by priority and ticket ID.

    Priority order:
        critical > high > medium > low

    Numeric ticket IDs are used to break priority ties.

    In-progress and resolved tickets are excluded.
    """
    if not isinstance(tickets, (list, tuple)):
        raise ValueError("Tickets must be provided as a list or tuple.")

    open_tickets = []

    for ticket in tickets:
        _validate_ticket(ticket)

        if ticket["status"] != "open":
            continue

        priority = ticket.get("priority")

        if not isinstance(priority, str):
            raise ValueError("A ticket has an invalid priority.")

        priority = priority.strip().casefold()

        if priority not in PRIORITY_ORDER:
            raise ValueError("A ticket has an invalid priority.")

        ticket_id = ticket.get("ticket_id")
        _ticket_id_sort_key(ticket_id)

        open_tickets.append(ticket)

    open_tickets.sort(
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"].strip().casefold()],
            _ticket_id_sort_key(ticket["ticket_id"]),
        )
    )

    return open_tickets