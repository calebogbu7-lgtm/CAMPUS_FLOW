# CampusFlow Design Decisions

## 1. Programming Language

We chose Python because it supports readable code, functions, dictionaries, file handling, and automated testing.

## 2. Ticket Data Structure

Each ticket is represented by a Python dictionary containing its ID, urgency, number of affected users, priority, status, and assigned staff member.

## 3. Priority Calculation

Ticket priority is calculated using urgency and the number of affected users. This helps the team identify tickets that need attention first.

## 4. Ticket Workflow

Tickets move through the statuses `open`, `in_progress`, and `resolved`. Validation helps prevent invalid status transitions, and a ticket must be assigned before work begins.

## 5. Work Queue

The work queue displays unresolved tickets in priority order. Tickets with the same priority should be ordered by their numeric ticket ID.

## 6. Data Persistence

We use JSON to store ticket information so that tickets can be loaded again when the application restarts.

## 7. Input Validation

The application validates ticket details, priorities, statuses, and staff assignments to reduce invalid data and unexpected behaviour.

## 8. Automated Testing

We use Python's `unittest` framework to test ticket creation, priority calculation, workflow operations, reporting, and data storage.

