"""Command-line interface for the CampusFlow helpdesk application."""

from campusflow.storage import load_tickets, save_tickets
from campusflow.ticket import create_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_report
from campusflow.search import search_tickets, sort_search_results
from campusflow.notes import add_note, get_ticket_notes
from campusflow.understanding_check import run_understanding_check


def display_ticket(ticket):
    """Display the details of a single ticket."""

    print("\n" + "=" * 45)
    print(f"Ticket ID:       {ticket.get('ticket_id', 'N/A')}")
    print(f"Title:           {ticket.get('title', 'N/A')}")
    print(f"Category:        {ticket.get('category', 'N/A')}")
    print(f"Urgency:         {ticket.get('urgency', 'N/A')}")
    print(f"Affected users:  {ticket.get('affected_users', 'N/A')}")
    print(f"Priority:        {ticket.get('priority', 'N/A')}")
    print(f"Status:          {ticket.get('status', 'N/A')}")
    print(f"Assigned to:     {ticket.get('assigned_to') or 'Unassigned'}")
    print("=" * 45)


def find_ticket_by_id(tickets, ticket_id):
    """Find a ticket by ID without requiring matching letter case."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        return None

    requested_id = ticket_id.strip().casefold()

    matches = [
        ticket
        for ticket in tickets
        if isinstance(ticket.get("ticket_id"), str)
        and ticket["ticket_id"].casefold() == requested_id
    ]

    if len(matches) != 1:
        return None

    return matches[0]


def create_new_ticket(tickets):
    """Collect ticket details and create a new ticket."""

    print("\n--- Create Ticket ---")

    title = input("Title: ").strip()
    category = input(
        "Category (Network, Hardware, Software, Other): "
    ).strip()
    urgency = input("Urgency (low, medium, high): ").strip()

    try:
        affected_users = int(input("Affected users: ").strip())

        ticket = create_ticket(
            title=title,
            category=category,
            urgency=urgency,
            affected_users=affected_users,
        )

        if find_ticket_by_id(tickets, ticket.get("ticket_id")) is not None:
            print("Could not create ticket: Duplicate ticket ID.")
            return

        tickets.append(ticket)

        try:
            save_tickets(tickets)
        except (OSError, ValueError, TypeError) as error:
            tickets.remove(ticket)
            print(f"Could not save the ticket: {error}")
            return

    except (ValueError, TypeError) as error:
        print(f"Could not create ticket: {error}")
        return
    except OSError as error:
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


def assign_existing_ticket(tickets):
    """Assign an existing ticket to a staff member."""

    print("\n--- Assign Ticket ---")

    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print("Could not assign ticket: Ticket not found.")
        return

    staff_name = input("Enter staff name: ").strip()

    try:
        assign_ticket(ticket, staff_name)
        save_tickets(tickets)
    except (ValueError, TypeError, OSError) as error:
        print(f"Could not assign ticket: {error}")
        return

    print("\nTicket assigned successfully.")
    display_ticket(ticket)


def change_ticket_status(tickets):
    """Update the status of an existing ticket."""

    print("\n--- Update Ticket Status ---")

    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print("Could not update status: Ticket not found.")
        return

    new_status = input(
        "New status (in_progress or resolved): "
    ).strip().casefold()

    if new_status == "in progress":
        new_status = "in_progress"

    try:
        update_status(ticket, new_status)
        save_tickets(tickets)
    except (ValueError, TypeError, OSError) as error:
        print(f"Could not update ticket status: {error}")
        return

    print("\nTicket status updated successfully.")
    display_ticket(ticket)


def show_work_queue(tickets):
    """Display the work queue returned by the workflow module."""

    print("\n--- Open Work Queue ---")

    try:
        queue = get_work_queue(tickets)
    except (ValueError, TypeError) as error:
        print(f"Could not retrieve the work queue: {error}")
        return

    if not queue:
        print("The work queue is empty.")
        return

    for ticket in queue:
        display_ticket(ticket)


def show_report(tickets):
    """Generate and display the ticket report."""

    print("\n--- Ticket Report ---")

    try:
        report = generate_report(tickets)

        # Support report functions that return text as well as
        # report functions that display the report themselves.
        if report is not None:
            print(report)

    except (ValueError, TypeError) as error:
        print(f"Could not generate report: {error}")


def search_existing_tickets(tickets):
    """Search tickets using a title and optional filters."""

    print("\n--- Search Tickets ---")
    print("Press Enter to skip an optional filter.")

    title_query = input("Title contains: ").strip()

    valid_categories = {
        "network",
        "hardware",
        "software",
        "other",
    }
    valid_statuses = {
        "open",
        "in_progress",
        "resolved",
    }
    valid_priorities = {
        "critical",
        "high",
        "medium",
        "low",
    }

    def get_optional_filter(prompt, valid_choices):
        """Collect an optional filter and validate its value."""

        while True:
            value = input(prompt).strip().casefold()

            if not value:
                return None

            if value in valid_choices:
                return value

            print(
                "Invalid choice. Enter one of: "
                + ", ".join(sorted(valid_choices))
                + ", or press Enter to skip."
            )

    category = get_optional_filter(
        "Category (Network, Hardware, Software, Other): ",
        valid_categories,
    )

    status = get_optional_filter(
        "Status (open, in_progress, resolved): ",
        valid_statuses,
    )

    priority = get_optional_filter(
        "Priority (critical, high, medium, low): ",
        valid_priorities,
    )

    try:
        results = search_tickets(
            tickets,
            title_query=title_query,
            category=category,
            status=status,
            priority=priority,
        )
    except (ValueError, TypeError) as error:
        print(f"Search failed: {error}")
        return

    if not results:
        print("No matching tickets found.")
        return

    while True:
        sort_choice = input(
            "Sort results by priority and ticket ID? (y/n): "
        ).strip().casefold()

        if sort_choice in ("y", "yes", "n", "no"):
            break

        print("Please enter y or n.")

    if sort_choice in ("y", "yes"):
        results = sort_search_results(results)

    print(f"\nFound {len(results)} matching ticket(s).")

    for ticket in results:
        display_ticket(ticket)


def add_ticket_note(tickets):
    """Collect details and add a note to an existing ticket."""

    print("\n--- Add Ticket Note ---")

    ticket_id = input("Enter ticket ID: ").strip()

    # Resolve the ID first so lowercase input also works.
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print("Could not add note: Ticket not found.")
        return

    author = input("Author name: ").strip()
    message = input("Note message: ").strip()

    # The note module requires the ticket's exact stored ID.
    actual_ticket_id = ticket["ticket_id"]

    try:
        note = add_note(
            tickets,
            actual_ticket_id,
            author,
            message,
        )

        save_tickets(tickets)

    except (ValueError, OSError, TypeError) as error:
        print(f"Could not add note: {error}")
        return

    print("\nNote added successfully.")
    print(f"Ticket ID: {actual_ticket_id}")
    print(f"Note ID: {note['note_id']}")
    print(f"Author:  {note['author']}")
    print(f"Message: {note['message']}")


def view_ticket_notes(tickets):
    """Display notes associated with a ticket."""

    print("\n--- View Ticket Notes ---")

    ticket_id = input("Enter ticket ID: ").strip()

    # Resolve the ID first so lowercase input also works.
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print("Could not retrieve notes: Ticket not found.")
        return

    # Pass the exact stored ID to the note module.
    actual_ticket_id = ticket["ticket_id"]

    try:
        notes = get_ticket_notes(tickets, actual_ticket_id)

    except (ValueError, TypeError) as error:
        print(f"Could not retrieve notes: {error}")
        return

    if not notes:
        print("No notes found for this ticket.")
        return

    print(f"\nNotes for ticket {actual_ticket_id}:")

    for note in notes:
        print("\n" + "-" * 40)
        print(f"Note ID: {note['note_id']}")
        print(f"Author:  {note['author']}")
        print(f"Message: {note['message']}")

    print("-" * 40)


def display_menu():
    """Display the main application menu."""

    print("\n========== CampusFlow ==========")
    print("1. Create ticket")
    print("2. List tickets")
    print("3. Assign ticket")
    print("4. Update ticket status")
    print("5. View open work queue")
    print("6. Generate report")
    print("7. Search tickets")
    print("8. Add ticket note")
    print("9. View ticket notes")
    print("10. Engineering Understanding Check")
    print("0. Exit")
    print("================================")


def main():
    """Run the CampusFlow command-line application."""

    try:
        tickets = load_tickets()

    except (OSError, ValueError, TypeError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Please check the ticket data file before continuing.")
        return

    while True:
        display_menu()
        choice = input("Choose an option (0-10): ").strip()

        if choice == "1":
            create_new_ticket(tickets)

        elif choice == "2":
            list_tickets(tickets)

        elif choice == "3":
            assign_existing_ticket(tickets)

        elif choice == "4":
            change_ticket_status(tickets)

        elif choice == "5":
            show_work_queue(tickets)

        elif choice == "6":
            show_report(tickets)

        elif choice == "7":
            search_existing_tickets(tickets)

        elif choice == "8":
            add_ticket_note(tickets)

        elif choice == "9":
            view_ticket_notes(tickets)

        elif choice == "10":
            run_understanding_check()

        elif choice == "0":
            print("Saving tickets before exit...")

            try:
                save_tickets(tickets)
            except (OSError, ValueError, TypeError) as error:
                print(f"Could not save tickets: {error}")
                continue

            print("Tickets saved. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from 0 to 10.")


if __name__ == "__main__":
    main()