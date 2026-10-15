"""Generate ticket statistics and reports for CampusFlow."""


VALID_STATUSES = ("open", "in_progress", "resolved")

VALID_PRIORITIES = ("critical", "high", "medium", "low")

VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")


def generate_report(tickets):
    """Generate summary statistics for the current collection of tickets.

    Args:
        tickets: A list of ticket dictionaries.

    Returns:
        A dictionary containing total counts, breakdowns by status,
        priority and category, unresolved and resolved counts,
        and the resolution percentage.

    Raises:
        ValueError: If a ticket contains an invalid status, priority,
            or category.
        KeyError: If a ticket is missing a required reporting field.
    """

    report = {
        "total_tickets": len(tickets),
        "by_status": {
            status: 0 for status in VALID_STATUSES
        },
        "by_priority": {
            priority: 0 for priority in VALID_PRIORITIES
        },
        "by_category": {
            category: 0 for category in VALID_CATEGORIES
        },
        "unresolved_tickets": 0,
        "resolved_tickets": 0,
        "resolution_percentage": 0.0,
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        category = ticket["category"]

        if status not in report["by_status"]:
            raise ValueError(f"Invalid ticket status: {status}")

        if priority not in report["by_priority"]:
            raise ValueError(f"Invalid ticket priority: {priority}")

        if category not in report["by_category"]:
            raise ValueError(f"Invalid ticket category: {category}")

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1
        report["by_category"][category] += 1

    report["resolved_tickets"] = report["by_status"]["resolved"]

    report["unresolved_tickets"] = (
        report["by_status"]["open"]
        + report["by_status"]["in_progress"]
    )

    if report["total_tickets"] > 0:
        report["resolution_percentage"] = round(
            (
                report["resolved_tickets"]
                / report["total_tickets"]
            ) * 100,
            2,
        )

    return report