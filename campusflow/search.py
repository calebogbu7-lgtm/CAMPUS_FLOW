"""Search CampusFlow tickets using optional filters and priority sorting."""

VALID_CATEGORIES = {"network", "hardware", "software", "other"}
VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def search_tickets(
    tickets,
    title="",
    category=None,
    status=None,
    priority=None,
):
    """Return tickets matching all supplied filters without modifying them."""

    if not isinstance(title, str):
        raise ValueError("Search title must be text.")

    # Remove surrounding whitespace from optional filter values.
    category = category.strip() if isinstance(category, str) else category
    status = status.strip() if isinstance(status, str) else status
    priority = priority.strip() if isinstance(priority, str) else priority

    # Empty optional filters mean no restriction.
    if category == "":
        category = None

    if status == "":
        status = None

    if priority == "":
        priority = None

    # Validate any filters that were actually supplied.
    if category is not None:
        if (
            not isinstance(category, str)
            or category.casefold() not in VALID_CATEGORIES
        ):
            raise ValueError("Invalid category filter.")

    if status is not None:
        if (
            not isinstance(status, str)
            or status.casefold() not in VALID_STATUSES
        ):
            raise ValueError("Invalid status filter.")

    if priority is not None:
        if (
            not isinstance(priority, str)
            or priority.casefold() not in VALID_PRIORITIES
        ):
            raise ValueError("Invalid priority filter.")

    search_title = title.strip().casefold()
    search_category = category.casefold() if category is not None else None
    search_status = status.casefold() if status is not None else None
    search_priority = priority.casefold() if priority is not None else None

    matching_tickets = []

    for ticket in tickets:
        if search_title and search_title not in ticket["title"].casefold():
            continue

        if (
            search_category is not None
            and ticket["category"].casefold() != search_category
        ):
            continue

        if (
            search_status is not None
            and ticket["status"].casefold() != search_status
        ):
            continue

        if (
            search_priority is not None
            and ticket["priority"].casefold() != search_priority
        ):
            continue

        matching_tickets.append(ticket)

    return matching_tickets


def sort_search_results(tickets):
    """Return tickets sorted by priority, then by numeric ticket ID."""

    def sorting_key(ticket):
        priority = ticket["priority"].casefold()
        ticket_id = ticket["ticket_id"]

        # Extract the numeric part of IDs such as T002 and T010.
        numeric_id = int(ticket_id[1:])

        return PRIORITY_ORDER[priority], numeric_id

    return sorted(tickets, key=sorting_key)