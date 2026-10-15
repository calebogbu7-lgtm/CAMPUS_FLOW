"""Tests for the CampusFlow Engineering Understanding Check."""

import unittest
from unittest.mock import patch

from campusflow.understanding_check import (
    QUESTIONS,
    get_valid_answer,
    run_understanding_check,
    score_answers,
)


class TestScoreAnswers(unittest.TestCase):
    """Test quiz scoring."""

    def test_all_correct_answers_score_six(self):
        answers = {
            1: "B",
            2: "C",
            3: "B",
            4: "C",
            5: "C",
            6: "B",
        }

        self.assertEqual(score_answers(answers), 6)

    def test_all_incorrect_answers_score_zero(self):
        answers = {
            1: "A",
            2: "A",
            3: "A",
            4: "A",
            5: "A",
            6: "A",
        }

        self.assertEqual(score_answers(answers), 0)

    def test_partially_correct_answers_score_two(self):
        answers = {
            1: "B",
            2: "A",
            3: "B",
        }

        self.assertEqual(score_answers(answers), 2)

    def test_lowercase_answers_are_accepted(self):
        answers = {
            1: "b",
            2: "c",
            3: "b",
            4: "c",
            5: "c",
            6: "b",
        }

        self.assertEqual(score_answers(answers), 6)

    def test_missing_answers_do_not_earn_points(self):
        answers = {
            1: "B",
        }

        self.assertEqual(score_answers(answers), 1)

    def test_question_bank_contains_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)


class TestGetValidAnswer(unittest.TestCase):
    """Test validation of multiple-choice answers."""

    @patch("builtins.input", side_effect=["X", "2", "b"])
    @patch("builtins.print")
    def test_invalid_choices_are_rejected_until_valid(
        self, mock_print, mock_input
    ):
        answer = get_valid_answer("Your answer: ")

        self.assertEqual(answer, "B")
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(mock_print.call_count, 2)

    @patch("builtins.input", return_value="  c  ")
    def test_spaces_and_lowercase_are_accepted(self, mock_input):
        answer = get_valid_answer("Your answer: ")

        self.assertEqual(answer, "C")


class TestRunUnderstandingCheck(unittest.TestCase):
    """Test the complete interactive quiz."""

    @patch(
        "builtins.input",
        side_effect=[
            "B", "C", "B", "C", "C", "B",
            "It protects ticket data.",
            "Zero tickets means there are no resolved tickets.",
        ],
    )
    @patch("builtins.print")
    def test_quiz_returns_score_and_collects_explanations(
        self, mock_print, mock_input
    ):
        score = run_understanding_check()

        self.assertEqual(score, 6)
        self.assertEqual(mock_input.call_count, 8)

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Your score: 6/6", printed_text)
        self.assertIn("It protects ticket data.", printed_text)
        self.assertIn(
            "Zero tickets means there are no resolved tickets.",
            printed_text,
        )

    @patch(
        "builtins.input",
        side_effect=[
            "B", "C", "B", "C", "C", "B",
            "", "Explanation for question one.",
            "Explanation for question two.",
        ],
    )
    @patch("builtins.print")
    def test_blank_explanation_is_rejected(
        self, mock_print, mock_input
    ):
        score = run_understanding_check()

        self.assertEqual(score, 6)
        self.assertEqual(mock_input.call_count, 9)

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn(
            "Please enter an explanation before continuing.",
            printed_text,
        )


if __name__ == "__main__":
    unittest.main()