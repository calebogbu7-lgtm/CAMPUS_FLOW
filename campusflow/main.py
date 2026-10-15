"""Command-line interface for the CampusFlow helpdesk application."""

from campusflow.ticket import create_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.search import search_tickets, sort_search_results


def display_ticket(ticket):
    """Display the details of a single ticket."""

    print("\n" + "-" * 48)
    print(f"Ticket ID:       {ticket['ticket_id']}")
    print(f"Title:           {ticket['title']}")
    print(f"Category:        {ticket['category']}")
    print(f"Urgency:         {ticket['urgency']}")
    print(f"Affected users:  {ticket['affected_users']}")
    print(f"Priority:        {ticket['priority']}")
    print(f"Status:          {ticket['status']}")
    print(f"Assigned to:     {ticket['assigned_to'] or 'Unassigned'}")
    print("-" * 48)


def find_ticket_by_id(tickets, ticket_id):
    """Find a ticket by ID without considering letter case."""

    ticket_id = ticket_id.strip().casefold()

    for ticket in tickets:
        if ticket["ticket_id"].casefold() == ticket_id:
            return ticket

    return None


def create_new_ticket(tickets):
    """Collect ticket details and add a new ticket."""

    print("\n--- Create Ticket ---")

    title = input("Title: ").strip()
    category = input(
        "Category (Network, Hardware, Software, Other): "
    ).strip()
    urgency = input("Urgency (low, medium, high): ").strip()

    try:
        affected_users = int(input("Affected users: ").strip())
    except ValueError:
        print("Invalid number of affected users.")
        return

    try:
        ticket = create_ticket(
            title=title,
            category=category,
            urgency=urgency,
            affected_users=affected_users,
        )
    except (ValueError, TypeError) as error:
        print(f"Could not create ticket: {error}")
        return

    if find_ticket_by_id(tickets, ticket["ticket_id"]):
        print(
            f"Could not create ticket: ID "
            f"{ticket['ticket_id']} already exists."
        )
        return

    tickets.append(ticket)
    print("Ticket created successfully.")


def list_tickets(tickets):
    """Display all tickets."""

    print("\n--- All Tickets ---")

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        display_ticket(ticket)


def assign_existing_ticket(tickets):
    """Assign an existing ticket to a staff member."""

    print("\n--- Assign Ticket ---")

    ticket_id = input("Ticket ID: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    staff_name = input("Staff member name: ").strip()

    try:
        assign_ticket(ticket, staff_name)
    except (ValueError, TypeError) as error:
        print(f"Could not assign ticket: {error}")
        return

    print("Ticket assigned successfully.")


def change_ticket_status(tickets):
    """Change the status of an existing ticket."""

    print("\n--- Update Ticket Status ---")

    ticket_id = input("Ticket ID: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    new_status = input(
        "New status (open, in_progress, resolved): "
    ).strip().casefold()

    if new_status == "in progress":
        new_status = "in_progress"

    try:
        update_status(ticket, new_status)
    except (ValueError, TypeError) as error:
        print(f"Could not update ticket status: {error}")
        return

    print("Ticket status updated successfully.")


def show_work_queue(tickets):
    """Display the priority-based work queue."""

    print("\n--- Open Work Queue ---")

    try:
        queue = get_work_queue(tickets)
    except (ValueError, TypeError) as error:
        print(f"Could not retrieve work queue: {error}")
        return

    if not queue:
        print("No tickets in the work queue.")
        return

    for ticket in queue:
        display_ticket(ticket)


def show_report(tickets):
    """Display a summary report of the tickets."""

    print("\n--- Ticket Report ---")

    try:
        report = generate_report(tickets)
    except (ValueError, TypeError) as error:
        print(f"Could not generate report: {error}")
        return

    if isinstance(report, dict):
        for key, value in report.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(report)


def search_existing_tickets(tickets):
    """Search tickets using a title and optional filters."""

    print("\n--- Search Tickets ---")

    title = input("Title contains (press Enter to skip): ").strip()
    category = input(
        "Category (Network/Hardware/Software/Other, "
        "press Enter to skip): "
    ).strip()
    status = input(
        "Status (open/in_progress/resolved, press Enter to skip): "
    ).strip()
    priority = input(
        "Priority (critical/high/medium/low, press Enter to skip): "
    ).strip()

    try:
        results = search_tickets(
            tickets,
            title=title,
            category=category,
            status=status,
            priority=priority,
        )
    except (ValueError, TypeError) as error:
        print(f"Could not search tickets: {error}")
        return

    if not results:
        print("No matching tickets found.")
        return

    print(f"\nFound {len(results)} matching ticket(s).")

    for ticket in results:
        display_ticket(ticket)

    sort_choice = input(
        "\nSort results by priority? (y/n): "
    ).strip().casefold()

    if sort_choice == "y":
        sorted_results = sort_search_results(results)

        print("\n--- Search Results Sorted by Priority ---")

        for ticket in sorted_results:
            display_ticket(ticket)


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
    print("8. Exit")
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
        choice = input("Choose an option (1-8): ").strip()

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
            try:
                save_tickets(tickets)
            except (OSError, ValueError, TypeError) as error:
                print(f"Could not save tickets: {error}")
                return

            print("Tickets saved. Goodbye!")
            break

        else:
            print("Invalid menu choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()