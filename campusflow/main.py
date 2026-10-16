from campusflow.ticket import create_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.notes import add_note, get_ticket_notes
from campusflow.search import search_tickets
from campusflow.understanding_check import run_understanding_check

def display_ticket(ticket):
    print(f"\nTicket ID: {ticket['ticket_id']}")
    print(f"Title: {ticket.get('title', 'Not provided')}")
    print(f"Category: {ticket.get('category', 'Not provided')}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket['assigned_to']}")


def create_new_ticket(tickets):
    try:
        title = input("Enter ticket title: ").strip()

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
        )

        ticket.setdefault("notes", [])

        tickets.append(ticket)

        try:
            save_tickets(tickets)
        except (OSError, ValueError) as error:
            tickets.remove(ticket)
            print(f"Error saving ticket: {error}")
            return

        print("\nTicket created successfully!")
        print(f"Your Ticket ID is: {ticket['ticket_id']}")
        display_ticket(ticket)

    except ValueError as error:
        print(f"Error: {error}")


def list_tickets(tickets):
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        display_ticket(ticket)


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            return ticket

    return None


def assign_existing_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    staff_name = input("Enter staff name: ").strip()

    try:
        assign_ticket(ticket, staff_name)
        save_tickets(tickets)
        print("Ticket assigned successfully.")
    except (ValueError, OSError) as error:
        print(f"Error: {error}")


def change_ticket_status(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    new_status = input(
        "New status (in_progress/resolved): "
    ).strip().lower()

    try:
        update_status(ticket, new_status)
        save_tickets(tickets)
        print("Ticket status updated successfully.")
    except (ValueError, OSError) as error:
        print(f"Error: {error}")


def show_work_queue(tickets):
    try:
        queue = get_work_queue(tickets)

        if not queue:
            print("\nNo unresolved tickets.")
            return

        print("\n--- WORK QUEUE ---")

        for ticket in queue:
            display_ticket(ticket)

    except ValueError as error:
        print(f"Error: {error}")


def show_report(tickets):
    try:
        report = generate_report(tickets)

        print("\n--- TICKET REPORT ---")
        print(f"Total tickets: {report['total_tickets']}")
        print(f"Resolved: {report['resolved_count']}")
        print(f"Unresolved: {report['unresolved_count']}")
        print(f"Resolution percentage: {report['resolution_percentage']}%")

        print("\nBy status:")
        for status, count in report["by_status"].items():
            print(f"{status}: {count}")

        print("\nBy priority:")
        for priority, count in report["by_priority"].items():
            print(f"{priority}: {count}")

        print("\nBy category:")
        for category, count in report["by_category"].items():
            print(f"{category}: {count}")

    except (KeyError, ValueError) as error:
        print(f"Error generating report: {error}")


def search_tickets_cli(tickets):
    query = input("Search title text (blank for all): ").strip()
    category = input("Category filter (Network/Hardware/Software/Other or blank): ").strip()
    status = input("Status filter (open/in_progress/resolved or blank): ").strip()
    priority = input("Priority filter (critical/high/medium/low or blank): ").strip()

    try:
        matches = search_tickets(
            tickets,
            query=query,
            category=category,
            status=status,
            priority=priority,
        )
    except ValueError as error:
        print(f"Search error: {error}")
        return

    if not matches:
        print("No matching tickets found.")
        return

    print("\n--- MATCHING TICKETS ---")
    for ticket in matches:
        display_ticket(ticket)


def run_understanding_check_cli():
    print("\n--- ENGINEERING UNDERSTANDING CHECK ---")
    result = run_understanding_check()
    print(f"\nCompleted. Final score: {result['score']}/{len(result['answers'])}")


def add_ticket_note(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    author = input("Enter your name: ").strip()
    message = input("Enter note: ").strip()

    try:
        add_note(tickets, ticket_id, author, message)
        save_tickets(tickets)
        print("Note added successfully.")

    except (ValueError, OSError) as error:
        print(f"Error: {error}")


def view_ticket_notes(tickets):
    ticket_id = input("Enter ticket ID: ").strip()

    try:
        notes = get_ticket_notes(tickets, ticket_id)

        if not notes:
            print("No notes found for this ticket.")
            return

        print(f"\n--- NOTES FOR {ticket_id} ---")

        for note in notes:
            print(f"\nNote ID: {note['note_id']}")
            print(f"Author: {note['author']}")
            print(f"Message: {note['message']}")

    except ValueError as error:
        print(f"Error: {error}")


def main():
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
        print("9. Search tickets")
        print("10. Engineering Understanding Check")
        print("11. Exit")

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
            search_tickets_cli(tickets)

        elif choice == "10":
            run_understanding_check_cli()

        elif choice == "11":
            try:
                save_tickets(tickets)
                print("CampusFlow closed. Goodbye!")
                break
            except (OSError, ValueError) as error:
                print(f"Error saving tickets: {error}")

        else:
            print("Invalid choice. Enter a number from 1 to 11.")


if __name__ == "__main__":
    main()