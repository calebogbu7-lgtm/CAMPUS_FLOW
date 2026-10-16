"""Business logic for CampusFlow ticket follow-up notes."""


def next_note_id(ticket):
    """Generate the next note ID without consuming it."""

    highest = 0

    for note in ticket.get("notes", []):
        note_id = note.get("note_id", "")

        if (
            isinstance(note_id, str)
            and note_id.startswith("N")
            and note_id[1:].isdigit()
        ):
            highest = max(highest, int(note_id[1:]))

    return f"N{highest + 1:03d}"


def add_note(tickets, ticket_id, author, message):
    """Add a validated note to an open or in-progress ticket."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("A valid ticket ID is required.")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Author cannot be blank.")

    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    author = author.strip()
    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError("Note message must contain 5–300 characters.")

    matches = [
        ticket for ticket in tickets
        if ticket.get("ticket_id") == ticket_id.strip()
    ]

    if len(matches) != 1:
        raise ValueError("Ticket not found or ticket ID is not unique.")

    ticket = matches[0]

    if ticket.get("status") not in ("open", "in_progress"):
        raise ValueError(
            "Only open or in-progress tickets can receive notes."
        )

    existing_notes = ticket.get("notes", [])

    if not isinstance(existing_notes, list):
        raise ValueError("Ticket notes must be a list.")

    existing_ids = set()

    for note in existing_notes:
        if not isinstance(note, dict):
            raise ValueError("Existing note data is invalid.")

        note_id = note.get("note_id")

        if (
            not isinstance(note_id, str)
            or not note_id.startswith("N")
            or not note_id[1:].isdigit()
        ):
            raise ValueError("An existing note has an invalid ID.")

        if note_id in existing_ids:
            raise ValueError("Duplicate note ID detected.")

        existing_ids.add(note_id)

    note_id = next_note_id(ticket)

    if note_id in existing_ids:
        raise ValueError("Duplicate note ID detected.")

    new_note = {
        "note_id": note_id,
        "author": author,
        "message": message,
    }

    ticket.setdefault("notes", []).append(new_note)

    return new_note


def get_ticket_notes(tickets, ticket_id):
    """Return ticket notes in numerical ID order."""

    matches = [
        ticket for ticket in tickets
        if ticket.get("ticket_id") == ticket_id
    ]

    if len(matches) != 1:
        raise ValueError("Ticket not found or ticket ID is not unique.")

    notes = matches[0].get("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be a list.")

    seen_ids = set()
    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("Invalid note data.")

        note_id = note.get("note_id")
        if (
            not isinstance(note_id, str)
            or not note_id.startswith("N")
            or not note_id[1:].isdigit()
            or note_id in seen_ids
        ):
            raise ValueError("Invalid or duplicate note ID.")

        if (
            not isinstance(note.get("author"), str)
            or not note["author"].strip()
            or not isinstance(note.get("message"), str)
            or not note["message"].strip()
        ):
            raise ValueError("Invalid note content.")

        seen_ids.add(note_id)

    return sorted(notes, key=lambda note: int(note["note_id"][1:]))
