import json
from pathlib import Path

from campusflow.ticket import sync_ticket_id

DEFAULT_FILE = Path("data/tickets.json")

REQUIRED_FIELDS = {
    "ticket_id",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}

VALID_URGENCIES = {"low", "medium", "high"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}


def validate_tickets(tickets):

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list.")

    seen_ids = set()

    for index, ticket in enumerate(tickets):
        if not isinstance(ticket, dict):
            raise ValueError(f"Ticket at index {index} must be an object.")

        missing = REQUIRED_FIELDS - ticket.keys()
        if missing:
            raise ValueError(
                f"Ticket at index {index} is missing fields: "
                f"{', '.join(sorted(missing))}."
            )

        ticket_id = ticket["ticket_id"]
        if (
            not isinstance(ticket_id, str)
            or len(ticket_id) < 4
            or not ticket_id.startswith("T")
            or not ticket_id[1:].isdigit()
        ):
            raise ValueError("Ticket ID must look like T001.")

        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}.")
        seen_ids.add(ticket_id)

        if ticket["urgency"] not in VALID_URGENCIES:
            raise ValueError(f"Invalid urgency for {ticket_id}.")

        users = ticket["affected_users"]
        if isinstance(users, bool) or not isinstance(users, int) or users <= 0:
            raise ValueError(f"Invalid affected-user count for {ticket_id}.")

        if ticket["priority"] not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority for {ticket_id}.")

        urgency = ticket["urgency"]
        expected_priority = (
            "critical"
            if urgency == "high" and users >= 10
            else "high"
            if urgency == "high" or users >= 10
            else "medium"
            if urgency == "medium" or users >= 3
            else "low"
        )
        if ticket["priority"] != expected_priority:
            raise ValueError(f"Priority does not match ticket data for {ticket_id}.")

        if ticket["status"] not in VALID_STATUSES:
            raise ValueError(f"Invalid status for {ticket_id}.")

        assigned_to = ticket["assigned_to"]
        if assigned_to is not None and (
            not isinstance(assigned_to, str) or not assigned_to.strip()
        ):
            raise ValueError(f"Invalid assignee for {ticket_id}.")

        if "title" in ticket and (
            not isinstance(ticket["title"], str) or not ticket["title"].strip()
        ):
            raise ValueError(f"Invalid title for {ticket_id}.")

        if "category" in ticket and ticket["category"] not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category for {ticket_id}.")

        if "notes" in ticket:
            notes = ticket["notes"]
            if not isinstance(notes, list):
                raise ValueError(f"Notes for {ticket_id} must be a list.")

            note_ids = set()
            for note in notes:
                if not isinstance(note, dict):
                    raise ValueError(f"Invalid note in ticket {ticket_id}.")

                note_id = note.get("note_id")
                if (
                    not isinstance(note_id, str)
                    or not note_id.startswith("N")
                    or not note_id[1:].isdigit()
                    or note_id in note_ids
                ):
                    raise ValueError(f"Invalid or duplicate note ID in {ticket_id}.")

                if (
                    not isinstance(note.get("author"), str)
                    or not note["author"].strip()
                    or not isinstance(note.get("message"), str)
                    or not note["message"].strip()
                ):
                    raise ValueError(f"Invalid note content in {ticket_id}.")

                note_ids.add(note_id)

    return True


def save_tickets(tickets, file_path=DEFAULT_FILE):


    validate_tickets(tickets)

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)

        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def load_tickets(file_path=DEFAULT_FILE):

    path = Path(file_path)

    if not path.exists():
        sync_ticket_id([])
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("Ticket data contains invalid JSON.") from error

    validate_tickets(tickets)
    sync_ticket_id(tickets)
    return tickets
