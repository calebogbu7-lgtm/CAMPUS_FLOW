"""Command-line interface for the CampusFlow helpdesk application."""

from copy import deepcopy
from pprint import pprint

from campusflow.storage import load_tickets, save_tickets
from campusflow.ticket import create_ticket
from campusflow.workflow import assign_ticket, get_work_queue, update_status
from campusflow.reports import generate_report
from campusflow.search import search_tickets, sort_search_results
from campusflow.notes import add_note, get_ticket_notes
from campusflow.understanding_check import run_understanding_check


CATEGORIES = {"network", "hardware", "software", "other"}
STATUSES = {"open", "in_progress", "resolved"}
PRIORITIES = {"critical", "high", "medium", "low"}
SAVE_ERRORS = (OSError, ValueError, TypeError)


def display_ticket(ticket):
    """Display the details of a single ticket."""
    print("\n" + "=" * 45)
    for label, key in (
        ("Ticket ID", "ticket_id"),
        ("Title", "title"),
        ("Category", "category"),
        ("Urgency", "urgency"),
        ("Affected users", "affected_users"),
        ("Priority", "priority"),
        ("Status", "status"),
    ):
        print(f"{label + ':':18}{ticket.get(key, 'N/A')}")

    print(f"{'Assigned to:':18}{ticket.get('assigned_to') or 'Unassigned'}")
    print("=" * 45)


def find_ticket_by_id(tickets, ticket_id):
    """Return exactly one case-insensitive ticket ID match, or None."""
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        return None

    requested_id = ticket_id.strip().casefold()
    matches = [
        ticket for ticket in tickets
        if isinstance(ticket, dict)
        and isinstance(ticket.get("ticket_id"), str)
        and ticket["ticket_id"].casefold() == requested_id
    ]
    return matches[0] if len(matches) == 1 else None


def ticket_id_exists(tickets, ticket_id):
    """Return whether a ticket ID already exists."""
    if not isinstance(ticket_id, str):
        return False

    requested_id = ticket_id.casefold()
    return any(
        isinstance(ticket, dict)
        and isinstance(ticket.get("ticket_id"), str)
        and ticket["ticket_id"].casefold() == requested_id
        for ticket in tickets
    )


def save_change(tickets, action, operation):
    """Run a ticket operation and save it, rolling back on failure."""
    original_tickets = deepcopy(tickets)

    try:
        operation()
        save_tickets(tickets)
    except (ValueError, TypeError, OSError, KeyError) as error:
        tickets[:] = original_tickets
        print(f"Could not {action}: {error}")
        return False

    return True


def request_ticket(tickets, action):
    """Ask for a ticket ID and return the matching ticket, if unique."""
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print(f"Could not {action}: Ticket not found or ID is ambiguous.")
    return ticket


def create_new_ticket(tickets):
    """Collect ticket details, create a ticket, and persist it."""
    print("\n--- Create Ticket ---")
    title = input("Title: ").strip()
    category = input("Category (Network, Hardware, Software, Other): ").strip()
    urgency = input("Urgency (low, medium, high): ").strip()

    try:
        affected_users = int(input("Affected users: ").strip())
        ticket = create_ticket(
            title=title,
            category=category,
            urgency=urgency,
            affected_users=affected_users,
        )
    except (ValueError, TypeError) as error:
        print(f"Could not create ticket: {error}")
        return

    if ticket_id_exists(tickets, ticket.get("ticket_id")):
        print("Could not create ticket: Duplicate ticket ID.")
        return

    tickets.append(ticket)
    try:
        save_tickets(tickets)
    except (OSError, ValueError, TypeError) as error:
        tickets.remove(ticket)
        print(f"Could not save the ticket: {error}")
        return

    print("\nTicket created successfully.")
    display_ticket(ticket)


def list_tickets(tickets):
    """Display all saved tickets."""
    print("\n--- All Tickets ---")
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        display_ticket(ticket)


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            return ticket

    return None


def assign_existing_ticket(tickets):
    """Assign a ticket to a staff member and persist the change."""
    print("\n--- Assign Ticket ---")
    ticket = request_ticket(tickets, "assign ticket")
    if ticket is None:
        return

    staff_name = input("Enter staff name: ").strip()
    if save_change(
        tickets,
        "assign ticket",
        lambda: assign_ticket(ticket, staff_name),
    ):
        print("\nTicket assigned successfully.")
        display_ticket(ticket)


def change_ticket_status(tickets):
    """Update a ticket's status through the workflow rules."""
    print("\n--- Update Ticket Status ---")
    ticket = request_ticket(tickets, "update status")
    if ticket is None:
        return

    new_status = input("New status (in_progress or resolved): ").strip().casefold()
    if new_status == "in progress":
        new_status = "in_progress"

    if save_change(
        tickets,
        "update ticket status",
        lambda: update_status(ticket, new_status),
    ):
        print("\nTicket status updated successfully.")
        display_ticket(ticket)


def reopen_existing_ticket(tickets):
    """Reopen a resolved ticket without changing the workflow module."""
    print("\n--- Reopen Resolved Ticket ---")
    ticket = request_ticket(tickets, "reopen ticket")
    if ticket is None:
        return

    def reopen():
        if ticket.get("status") != "resolved":
            raise ValueError("Only resolved tickets can be reopened.")
        ticket["status"] = "open"

    if save_change(tickets, "reopen ticket", reopen):
        print("\nTicket reopened successfully.")
        display_ticket(ticket)


def show_work_queue(tickets):
    """Display open tickets in priority order."""
    print("\n--- Open Work Queue ---")

    try:
        open_tickets = get_work_queue(tickets)
    except (ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"Could not retrieve the work queue: {error}")
        return

    if not open_tickets:
        print("The open work queue is empty.")
        return

    for ticket in open_tickets:
        display_ticket(ticket)


def show_report(tickets):
    """Generate and display the ticket report."""
    print("\n--- Ticket Report ---")

    try:
        report = generate_report(tickets)
        if report is not None:
            pprint(report) if isinstance(report, (dict, list, tuple)) else print(report)
    except (ValueError, TypeError, KeyError) as error:
        print(f"Could not generate report: {error}")


def get_optional_filter(prompt, valid_choices):
    """Collect a valid optional search filter."""
    while True:
        value = input(prompt).strip().casefold()
        if not value:
            return None

        if value == "in progress":
            value = "in_progress"

        if value in valid_choices:
            return value

        choices = ", ".join(sorted(valid_choices))
        print(f"Invalid choice. Enter one of: {choices}, or press Enter to skip.")


def search_existing_tickets(tickets):
    """Search tickets with optional filters and sorting."""
    print("\n--- Search Tickets ---")
    print("Press Enter to skip an optional filter.")
    title_query = input("Title contains: ").strip()

    category = get_optional_filter(
        "Category (Network, Hardware, Software, Other): ", CATEGORIES
    )
    status = get_optional_filter(
        "Status (open, in_progress, resolved): ", STATUSES
    )
    priority = get_optional_filter(
        "Priority (critical, high, medium, low): ", PRIORITIES
    )

    try:
        results = search_tickets(
            tickets,
            title=title_query,
            category=category,
            status=status,
            priority=priority,
        )
    except (ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"Search failed: {error}")
        return

    if not results:
        print("No matching tickets found.")
        return

    while True:
        choice = input("Sort results by priority and ticket ID? (y/n): ")
        choice = choice.strip().casefold()
        if choice in {"y", "yes", "n", "no"}:
            break
        print("Please enter y or n.")

    if choice in {"y", "yes"}:
        try:
            results = sort_search_results(results)
        except (ValueError, TypeError, KeyError, AttributeError) as error:
            print(f"Could not sort search results: {error}")
            return

    print(f"\nFound {len(results)} matching ticket(s).")
    for ticket in results:
        display_ticket(ticket)


def add_ticket_note(tickets):
    """Add a note to a ticket and persist it."""
    print("\n--- Add Ticket Note ---")
    ticket = request_ticket(tickets, "add note")
    if ticket is None:
        return

    author = input("Author name: ").strip()
    message = input("Note message: ").strip()
    ticket_id = ticket["ticket_id"]
    result = {}

    def add_and_capture_note():
        result["note"] = add_note(tickets, ticket_id, author, message)

    if not save_change(tickets, "add note", add_and_capture_note):
        return

    note = result["note"]
    print("\nNote added successfully.")
    print(f"Ticket ID: {ticket_id}")
    print(f"Note ID: {note['note_id']}")
    print(f"Author:  {note['author']}")
    print(f"Message: {note['message']}")


def view_ticket_notes(tickets):
    """Display notes associated with a ticket."""
    print("\n--- View Ticket Notes ---")
    ticket = request_ticket(tickets, "retrieve notes")
    if ticket is None:
        return

    try:
        notes = get_ticket_notes(tickets, ticket["ticket_id"])
    except (ValueError, TypeError, KeyError) as error:
        print(f"Could not retrieve notes: {error}")
        return

    if not notes:
        print("No notes found for this ticket.")
        return

    print(f"\nNotes for ticket {ticket['ticket_id']}:")
    for note in notes:
        print("\n" + "-" * 40)
        print(f"Note ID: {note['note_id']}")
        print(f"Author:  {note['author']}")
        print(f"Message: {note['message']}")
    print("-" * 40)


def display_menu():
    """Display the main CampusFlow menu."""
    print(
        "\n========== CampusFlow =========="
        "\n1. Create ticket\n"
        "2. List tickets\n"
        "3. Assign ticket\n"
        "4. Update ticket status\n"
        "5. View open work queue\n"
        "6. Generate report\n"
        "7. Search tickets\n"
        "8. Add ticket note\n"
        "9. View ticket notes\n"
        "10. Engineering Understanding Check\n"
        "11. Reopen resolved ticket\n"
        "0. Save and exit\n"
        "================================"
    )


def main():
    """Load saved tickets and run the interactive CLI."""
    try:
        tickets = load_tickets()
    except (OSError, ValueError, TypeError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Please check the ticket data file before continuing.")
        return

    actions = {
        "1": create_new_ticket,
        "2": list_tickets,
        "3": assign_existing_ticket,
        "4": change_ticket_status,
        "5": show_work_queue,
        "6": show_report,
        "7": search_existing_tickets,
        "8": add_ticket_note,
        "9": view_ticket_notes,
        "10": lambda _: run_understanding_check(),
        "11": reopen_existing_ticket,
    }

    while True:
        display_menu()
        try:
            choice = input("Choose an option (0-11): ").strip()
        except EOFError:
            print("\nInput closed. Attempting to save before exiting.")
            try:
                save_tickets(tickets)
            except SAVE_ERRORS as error:
                print(f"Could not save tickets: {error}")
                return
            print("Tickets saved. Goodbye!")
            return

        if choice == "0":
            try:
                save_tickets(tickets)
            except SAVE_ERRORS as error:
                print(f"Could not save tickets: {error}")
                continue
            print("Tickets saved. Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please choose a number from 0 to 11.")
            continue

        action(tickets)


if __name__ == "__main__":
    main()
