"""Engineering Understanding Check for CampusFlow Next."""

QUESTION_BANK = [
    {
        "question": "Ticket T001 is open and unassigned. A user tries to move it to in_progress.",
        "choices": {
            "A": "Accept",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove ticket",
        },
        "answer": "B",
    },
    {
        "question": "The app has zero tickets. What should resolution percentage display?",
        "choices": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
    },
    {
        "question": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "choices": {
            "A": "Any record matching one filter",
            "B": "Only records matching all supplied filters",
            "C": "All network records",
            "D": "All open records",
        },
        "answer": "B",
    },
    {
        "question": "A resolved ticket receives 'Add note'. What should happen?",
        "choices": {
            "A": "Append anyway",
            "B": "Delete old notes",
            "C": "Reject until reopened",
            "D": "Change status silently",
        },
        "answer": "C",
    },
    {
        "question": "The JSON file includes two tickets with the same ID. What should load do?",
        "choices": {
            "A": "Keep both",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename IDs silently",
        },
        "answer": "C",
    },
    {
        "question": "A PR changes validation but has no negative-case tests. Best review action?",
        "choices": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "answer": "B",
    },
]


def grade_answers(submitted_answers):
    """Return the score for a list of submitted answer letters."""
    total = 0
    for index, answer in enumerate(submitted_answers[: len(QUESTION_BANK)]):
        candidate = str(answer or "").strip().upper()
        if candidate == QUESTION_BANK[index]["answer"]:
            total += 1
    return total


def _prompt_for_choice(question, input_func, output_func):
    while True:
        output_func(f"\n{question['question']}")
        for key, value in question["choices"].items():
            output_func(f"{key}. {value}")

        choice = input_func("Choose A/B/C/D: ").strip().upper()
        if choice in {"A", "B", "C", "D"}:
            return choice

        output_func("Invalid choice. Please enter A, B, C, or D.")


def _request_explanation(index, answer, input_func, output_func):
    while True:
        output_func(
            f"\nExplain question {index + 1} briefly: "
            f"Why is the answer {answer} correct?"
        )
        explanation = input_func("Your explanation: ").strip()
        if len(explanation) >= 5:
            return explanation
        output_func("Please provide a short explanation of at least 5 characters.")


def run_understanding_check(input_func=None, output_func=None):
    """Run the Engineering Understanding Check and return a score + explanations."""
    if input_func is None:
        import builtins
        input_func = builtins.input
    if output_func is None:
        output_func = print

    submitted_answers = []

    for question in QUESTION_BANK:
        submitted_answers.append(_prompt_for_choice(question, input_func, output_func))

    score = grade_answers(submitted_answers)
    explanations = []

    output_func(f"\nFinal score: {score}/{len(QUESTION_BANK)}")

    for index, answer in enumerate(submitted_answers[:2]):
        explanation = _request_explanation(index, answer, input_func, output_func)
        explanations.append({
            "question_number": index + 1,
            "answer": answer,
            "explanation": explanation,
        })

    output_func("\nLearning notes:")
    for entry in explanations:
        output_func(
            f"Q{entry['question_number']}: {entry['answer']} - {entry['explanation']}"
        )

    return {
        "score": score,
        "answers": submitted_answers,
        "explanations": explanations,
    }
