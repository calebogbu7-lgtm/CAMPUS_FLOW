from notes import add_note, get_ticket_notes
from ticket import create_ticket
from workflow import assign_ticket, update_status, get_work_queue
from reports import generate_report
from storage import load_tickets, save_tickets


def display_ticket(ticket):
    """Display the details of a ticket."""
    print(f"\nTicket ID: {ticket['ticket_id']}")
    print(f"Title: {ticket.get('title', 'Not provided')}")
    print(f"Category: {ticket.get('category', 'Not provided')}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket['assigned_to']}")


def create_new_ticket(tickets):
    """Create a new helpdesk ticket."""
    try:
        title = input("Enter ticket title: ").strip()

        if not title:
            print("Error: Ticket title cannot be blank.")
            return

        print("\nSelect ticket category:")
        print("1. Network")
        print("2. Hardware")
        print("3. Software")
        print("4. Other")

        categories = {
            "1": "Network",
            "2": "Hardware",
            "3": "Software",
            "4": "Other",
        }

        category_choice = input("Choose category (1-4): ").strip()

        if category_choice not in categories:
            print("Error: Invalid category selection.")
            return

        category = categories[category_choice]

        urgency = input(
            "Urgency (low/medium/high): "
        ).strip().lower()

        affected_users_input = input(
            "Number of affected users: "
        ).strip()

        try:
            affected_users = int(affected_users_input)
        except ValueError:
            print("Error: Affected users must be a whole number.")
            return

        ticket = create_ticket(
            title=title,
            category=category,
            urgency=urgency,
            affected_users=affected_users,
            tickets=tickets,
        )

        tickets.append(ticket)
        save_tickets(tickets)

        print("\nTicket created successfully.")
        display_ticket(ticket)

    except (ValueError, TypeError, OSError) as error:
        print(f"Error creating ticket: {error}")


def list_tickets(tickets):
    """Display all tickets."""
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        display_ticket(ticket)


def assign_existing_ticket(tickets):
    """Assign a ticket to a staff member."""
    ticket_id = input("Enter ticket ID: ").strip()
    staff_name = input("Enter staff name: ").strip()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            try:
                assign_ticket(ticket, staff_name)
                save_tickets(tickets)
                print("Ticket assigned successfully.")
            except (ValueError, TypeError, OSError) as error:
                print(f"Error assigning ticket: {error}")
            return

    print("Ticket not found.")


def change_ticket_status(tickets):
    """Update the status of a ticket."""
    ticket_id = input("Enter ticket ID: ").strip()

    new_status = input(
        "New status (in_progress/resolved): "
    ).strip().lower()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            try:
                update_status(ticket, new_status)
                save_tickets(tickets)
                print("Ticket status updated successfully.")
            except (ValueError, TypeError, OSError) as error:
                print(f"Error updating status: {error}")
            return

    print("Ticket not found.")


def show_work_queue(tickets):
    """Display unresolved tickets."""
    try:
        queue = get_work_queue(tickets)

        if not queue:
            print("\nNo unresolved tickets.")
            return

        print("\n--- WORK QUEUE ---")

        for ticket in queue:
            display_ticket(ticket)

    except (ValueError, TypeError) as error:
        print(f"Error displaying work queue: {error}")


def show_report(tickets):
    """Display a summary of tickets."""
    try:
        report = generate_report(tickets)

        print("\n--- TICKET REPORT ---")
        print(f"Total tickets: {report['total_tickets']}")

        print("\nBy status:")
        for status, count in report["by_status"].items():
            print(f"{status}: {count}")

        print("\nBy priority:")
        for priority, count in report["by_priority"].items():
            print(f"{priority}: {count}")

    except (KeyError, ValueError, TypeError) as error:
        print(f"Error generating report: {error}")


def add_ticket_note(tickets):
    """Add a note to an existing ticket."""
    ticket_id = input("Enter ticket ID: ").strip()
    author = input("Enter your name: ").strip()
    message = input("Enter your note: ").strip()

    try:
        add_note(tickets, ticket_id, author, message)
        save_tickets(tickets)
        print("Note added successfully.")

    except (ValueError, TypeError, OSError) as error:
        print(f"Error adding note: {error}")


def view_ticket_notes(tickets):
    """Display notes for a ticket."""
    ticket_id = input("Enter ticket ID: ").strip()

    try:
        notes = get_ticket_notes(tickets, ticket_id)

        if not notes:
            print("No notes found for this ticket.")
            return

        print(f"\n--- NOTES FOR TICKET {ticket_id} ---")

        for note in notes:
            print(f"\nNote ID: {note['note_id']}")
            print(f"Author: {note['author']}")
            print(f"Message: {note['message']}")

    except (ValueError, TypeError) as error:
        print(f"Error viewing notes: {error}")


def main():
    """Run the CampusFlow helpdesk application."""
    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Could not load saved tickets: {error}")
        return

    while True:
        print("\n===== CAMPUSFLOW HELPDESK =====")
        print("1. Create ticket")
        print("2. List tickets")
        print("3. Assign ticket")
        print("4. Update ticket status")
        print("5. View work queue")
        print("6. Generate report")
        print("7. Add note")
        print("8. View ticket notes")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

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
            add_ticket_note(tickets)

        elif choice == "8":
            view_ticket_notes(tickets)

        elif choice == "9":
            try:
                save_tickets(tickets)
            except (ValueError, OSError) as error:
                print(f"Error saving tickets: {error}")
                continue

            print("CampusFlow closed. Goodbye!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 9.")


if __name__ == "__main__":
    main()