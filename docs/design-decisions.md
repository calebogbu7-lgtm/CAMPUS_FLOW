# CampusFlow Design Decisions

## 1. Programming Language

We chose Python because it supports readable code, functions, dictionaries, file handling, and automated testing. These features are suitable for building a command-line helpdesk application.

## 2. Ticket Data Structure

We represent each ticket using a Python dictionary. Each ticket contains information such as its ID, urgency, number of affected users, priority, status, and assigned staff member.

This makes it straightforward to access and update ticket information.

## 3. Priority Calculation

Ticket priority is determined by urgency and the number of affected users. This allows tickets requiring more urgent attention to be identified and handled first.

## 4. Ticket Workflow

Tickets follow a controlled workflow from open to in_progress and then resolved. We validate status changes to prevent invalid transitions. A ticket must also be assigned before work can begin.

## 5. Work Queue

The work queue excludes resolved tickets and sorts unresolved tickets by priority. Ticket IDs are used to order tickets with the same priority.

## 6. Data Persistence

We use JSON file storage to preserve ticket information between application runs. This allows the application to reload previously created tickets instead of losing them when it closes.

## 7. Error Handling and Validation

We validate user input and ticket data to reduce invalid records and unexpected behaviour. Errors such as invalid priorities, statuses, and staff assignments should be handled clearly.

## 8. Automated Testing

We use Python's unittest framework to test ticket creation, priority calculation, workflow operations, reporting, and data storage. Automated tests help us identify errors and confirm that the application behaves as expected.
