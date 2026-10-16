def generate_report(tickets):
    report = {
        "total_tickets": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
        "by_category": {
            "Network": 0,
            "Hardware": 0,
            "Software": 0,
            "Other": 0,
        },
        "unresolved_count": 0,
        "resolved_count": 0,
        "resolution_percentage": 0,
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        category = ticket.get("category", "Other")

        if status not in report["by_status"]:
            raise ValueError(f"Invalid ticket status: {status}")

        if priority not in report["by_priority"]:
            raise ValueError(f"Invalid ticket priority: {priority}")

        if category not in report["by_category"]:
            raise ValueError(f"Invalid ticket category: {category}")

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1
        report["by_category"][category] += 1

        if status == "resolved":
            report["resolved_count"] += 1
        elif status in {"open", "in_progress"}:
            report["unresolved_count"] += 1

    if report["total_tickets"]:
        report["resolution_percentage"] = round(
            (report["resolved_count"] / report["total_tickets"]) * 100,
            2,
        )

    return report
