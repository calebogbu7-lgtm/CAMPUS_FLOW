import json
from pathlib import Path

DEFAULT_FILE = Path("data/tickets.json")


def save_tickets(tickets, file_path=DEFAULT_FILE):
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
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError("Ticket data contains invalid JSON.") from error

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list.")

    return tickets
