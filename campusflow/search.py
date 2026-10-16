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
    """Return tickets matching all supplied filters.

    Title matching is case-insensitive and supports partial matches.
    Category, status, and priority filters are optional and are combined
    using AND logic. Empty filters impose no restriction.

    The function does not modify the original ticket collection.

    Args:
        tickets: An iterable of ticket dictionaries.
        title: Optional full or partial title to search for.
        category: Optional category filter.
        status: Optional status filter.
        priority: Optional priority filter.

    Returns:
        A list containing the matching ticket dictionaries.

    Raises:
        ValueError: If a supplied filter has an invalid type or value.
        KeyError: If a ticket is missing a required search field.
        AttributeError: If a required ticket field does not support
            the expected string operations.
    """
    if not isinstance(title, str):
        raise ValueError("Search title must be text.")

    # Normalise optional filters without changing the original arguments.
    category = _normalise_filter(
        category,
        VALID_CATEGORIES,
        "category",
    )
    status = _normalise_filter(
        status,
        VALID_STATUSES,
        "status",
    )
    priority = _normalise_filter(
        priority,
        VALID_PRIORITIES,
        "priority",
    )

    search_title = title.strip().casefold()

    matching_tickets = []

    for ticket in tickets:
        ticket_title = ticket["title"].casefold()
        ticket_category = ticket["category"].casefold()
        ticket_status = ticket["status"].casefold()
        ticket_priority = ticket["priority"].casefold()

        if search_title and search_title not in ticket_title:
            continue

        if category is not None and ticket_category != category:
            continue

        if status is not None and ticket_status != status:
            continue

        if priority is not None and ticket_priority != priority:
            continue

        matching_tickets.append(ticket)

    return matching_tickets


def _normalise_filter(value, valid_values, filter_name):
    """Validate and normalise an optional search filter.

    An omitted or empty filter means that no restriction is applied.
    Valid values are compared without case sensitivity.

    Args:
        value: The filter value supplied by the caller.
        valid_values: The permitted lowercase filter values.
        filter_name: The filter name used in error messages.

    Returns:
        The normalised lowercase value, or None for an empty filter.

    Raises:
        ValueError: If the filter value is not a string or is invalid.
    """
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(
            f"Search {filter_name} filter must be text."
        )

    normalised_value = value.strip().casefold()

    if not normalised_value:
        return None

    if normalised_value not in valid_values:
        raise ValueError(
            f"Invalid {filter_name} filter: {value}"
        )

    return normalised_value


def sort_search_results(tickets):
    """Return tickets sorted by priority and numeric ticket ID.

    Tickets with higher priority appear first. Tickets with the same
    priority are ordered by the numeric portion of their ticket IDs.

    The original collection is not modified.

    Args:
        tickets: An iterable of ticket dictionaries.

    Returns:
        A new list sorted by priority and numeric ticket ID.

    Raises:
        KeyError: If a ticket is missing its priority or ticket ID.
        ValueError: If a ticket ID has no valid numeric portion or its
            priority is not recognised.
        TypeError: If the supplied ticket ID or priority has an
            incompatible type.
    """

    def sorting_key(ticket):
        priority = ticket["priority"]

        if not isinstance(priority, str):
            raise ValueError("Ticket priority must be text.")

        normalised_priority = priority.casefold()

        if normalised_priority not in PRIORITY_ORDER:
            raise ValueError(
                f"Invalid ticket priority: {priority}"
            )

        ticket_id = ticket["ticket_id"]

        if not isinstance(ticket_id, str):
            raise ValueError("Ticket ID must be text.")

        # Support IDs such as T001 and T010.
        # The prefix must be followed by a numeric portion.
        numeric_part = ticket_id[1:]

        if (
            len(ticket_id) < 2
            or not ticket_id[0].isalpha()
            or not numeric_part.isdigit()
        ):
            raise ValueError(
                f"Invalid ticket ID: {ticket_id}"
            )

        numeric_id = int(numeric_part)

        return PRIORITY_ORDER[normalised_priority], numeric_id

    return sorted(tickets, key=sorting_key)