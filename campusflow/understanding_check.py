"""Engineering Understanding Check for CampusFlow."""


QUESTIONS = [
    {
        "id": 1,
        "question": (
            "T001 is open and unassigned. Someone tries to move it "
            "to in_progress. What should happen?"
        ),
        "options": {
            "A": "Accept the change.",
            "B": "Reject the change and preserve all data.",
            "C": "Resolve the ticket automatically.",
            "D": "Remove the ticket.",
        },
        "correct_answer": "B",
    },
    {
        "id": 2,
        "question": (
            "CampusFlow has zero tickets. What should the resolution "
            "percentage be?"
        ),
        "options": {
            "A": "Crash.",
            "B": "100%.",
            "C": "0%.",
            "D": "Divide by one without explanation.",
        },
        "correct_answer": "C",
    },
    {
        "id": 3,
        "question": (
            "A user searches for title 'wifi', category 'Network', "
            "and status 'open'. How should the filters work?"
        ),
        "options": {
            "A": "Match any one filter.",
            "B": "Match all three filters.",
            "C": "Match every Network ticket.",
            "D": "Match every open ticket.",
        },
        "correct_answer": "B",
    },
    {
        "id": 4,
        "question": (
            "Someone tries to add a note to a resolved ticket. "
            "What should happen?"
        ),
        "options": {
            "A": "Append the note.",
            "B": "Delete the ticket's existing notes.",
            "C": "Reject the note until the ticket is reopened.",
            "D": "Silently change the ticket's status.",
        },
        "correct_answer": "C",
    },
    {
        "id": 5,
        "question": (
            "A JSON file contains duplicate ticket IDs. What should "
            "a safe load operation do?"
        ),
        "options": {
            "A": "Keep both tickets.",
            "B": "Replace memory with the duplicate tickets.",
            "C": "Reject the load without changing existing memory.",
            "D": "Rename the IDs silently.",
        },
        "correct_answer": "C",
    },
    {
        "id": 6,
        "question": (
            "A pull request changes validation but has no tests for "
            "invalid inputs. What is the best review action?"
        ),
        "options": {
            "A": "Approve because the code runs.",
            "B": "Request focused tests and an explanation of the change.",
            "C": "Merge immediately.",
            "D": "Ask AI to approve it.",
        },
        "correct_answer": "B",
    },
]


def score_answers(answers):
    """Calculate the quiz score.

    Args:
        answers: A dictionary mapping question IDs to answer letters.

    Returns:
        The number of correct answers, from 0 to 6.
    """
    score = 0

    for question in QUESTIONS:
        question_id = question["id"]
        correct_answer = question["correct_answer"]
        user_answer = answers.get(question_id, "").strip().upper()

        if user_answer == correct_answer:
            score += 1

    return score


def get_valid_answer(prompt):
    """Ask repeatedly until the user enters A, B, C, or D."""
    valid_choices = {"A", "B", "C", "D"}

    while True:
        answer = input(prompt).strip().upper()

        if answer in valid_choices:
            return answer

        print("Invalid choice. Please enter A, B, C, or D.")


def run_understanding_check():
    """Run the quiz, collect explanations, and display mentor notes."""
    answers = {}
    explanations = {}

    print("\n=== CampusFlow Engineering Understanding Check ===")
    print("Choose A, B, C, or D for each question.\n")

    for question in QUESTIONS:
        question_id = question["id"]

        print(f"Question {question_id}: {question['question']}")

        for letter, option in question["options"].items():
            print(f"  {letter}. {option}")

        answer = get_valid_answer("Your answer: ")
        answers[question_id] = answer
        print()

    score = score_answers(answers)

    print("=== Quiz Results ===")
    print(f"Your score: {score}/{len(QUESTIONS)}")

    print("\n=== Explain Your Reasoning ===")
    print("Explain at least two of your answers in your own words.")

    for question_id in (1, 2):
        while True:
            explanation = input(
                f"Explain why you chose {answers[question_id]} "
                f"for Question {question_id}: "
            ).strip()

            if explanation:
                explanations[question_id] = explanation
                break

            print("Please enter an explanation before continuing.")

    print("\n=== Mentor Discussion Notes ===")

    for question_id, explanation in explanations.items():
        print(f"Question {question_id}: {explanation}")

    return score