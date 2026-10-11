# AI Learning Log — Engineer A

## Entry 1: Ticket Creation and Priority

**Task:** Implement ticket creation and priority calculation.

**AI assistance:** I used AI to understand how to structure ticket data and calculate priority from urgency and the number of affected users.

**What I learned:** A function can validate ticket information and calculate a priority before creating a ticket.

**Verification:** I ran the ticket tests to check ticket creation, validation, and priority calculation.

**Outcome:** I learned how to separate validation and priority calculation into reusable functions.

## Entry 2: Input Validation

**Task:** Validate ticket information.

**AI assistance:** I used AI to explore possible invalid inputs and how to handle them.

**What I learned:** Input validation prevents invalid urgency values and affected-user counts from being accepted.

**Verification:** I checked the validation logic and relevant ticket tests, including invalid input cases.

**Outcome:** I understood why validation should happen before a ticket is created.

## Entry 3: Testing and Checking AI Suggestions

**Task:** Verify that the ticket functionality works with the integrated project.

**AI assistance:** I used AI to help understand test execution and troubleshoot Python imports.

**What I checked:** I compared the suggested test command with the project folder structure.

**Correction or improvement:** The initial test command needed the correct Python module path. I used `PYTHONPATH=campusflow` with unittest discovery to run the integrated tests successfully.

**Testing:** `PYTHONPATH=campusflow python3 -m unittest discover -s campusflow/tests -v`

**Result:** 25 tests passed.

**Outcome:** I learned to verify AI suggestions against the actual project structure and confirm changes by running tests.
