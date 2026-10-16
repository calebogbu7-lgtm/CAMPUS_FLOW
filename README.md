# CAMPUS_FLOW C_F
# CampusFlow

CampusFlow is a command-line helpdesk ticket management application
built with Python. It helps users create, manage, assign, and track
support tickets.

## Engineer A: Ticket Validation and Storage (engr caleb ogbu)

Engineer A is responsible for improving ticket data integrity,
validating user input, protecting ticket workflows, and ensuring
reliable JSON storage.

### Responsibilities

- Validate ticket fields, including title, category, urgency, and
  affected-user count.
- Calculate ticket priority according to the project's business rules.
- Validate ticket data before saving or processing it.
- Protect workflow operations against invalid status changes.
- Validate ticket notes and their associated data.
- Save ticket information to JSON storage.
- Load saved tickets when the application restarts.
- Preserve unique ticket IDs across application restarts.
- Handle invalid or malformed stored data safely.

### Technologies

- Python
- JSON
- Git and GitHub
- Python `unittest`

## Project Structure

```text
CAMPUS_FLOW/
├── campusflow/
│   ├── main.py
│   ├── ticket.py
│   ├── workflow.py
│   ├── storage.py
│   ├── reports.py
│   └── notes.py
├── tests/
├── docs/
└── README.md