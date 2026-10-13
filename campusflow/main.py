from ticket import create_ticket
from workflow import assign_ticket, update_status, get_work_queue
from reports import generate_report
from storage import load_tickets, save_tickets


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
        )

        tickets.append(ticket)
        save_tickets(tickets)

        print("\nTicket created successfully.")
        display_ticket(ticket)

    except ValueError as error:
        print(f"Error: {error}")


def list_tickets(tickets):
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        display_ticket(ticket)


def assign_existing_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    staff_name = input("Enter staff name: ").strip()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            try:
                assign_ticket(ticket, staff_name)
                save_tickets(tickets)
                print("Ticket assigned successfully.")
            except ValueError as error:
                print(f"Error: {error}")
            return

    print("Ticket not found.")


def change_ticket_status(tickets):
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
            except ValueError as error:
                print(f"Error: {error}")
            return

    print("Ticket not found.")


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

        print("\nBy status:")
        for status, count in report["by_status"].items():
            print(f"{status}: {count}")

        print("\nBy priority:")
        for priority, count in report["by_priority"].items():
            print(f"{priority}: {count}")

    except (KeyError, ValueError) as error:
        print(f"Error generating report: {error}")


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
        print("7. Exit")

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
            save_tickets(tickets)
            print("CampusFlow closed. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()