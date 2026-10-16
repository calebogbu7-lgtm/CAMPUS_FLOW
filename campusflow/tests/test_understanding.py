import unittest
from unittest.mock import patch

from campusflow.understanding_check import (
    QUESTION_BANK,
    grade_answers,
    run_understanding_check,
)


class TestUnderstandingCheck(unittest.TestCase):

    def test_question_bank_has_six_questions(self):
        self.assertEqual(len(QUESTION_BANK), 6)

    def test_invalid_answer_is_retried_and_score_is_correct(self):
        answers = iter(["B", "z", "A", "C", "C", "B", "", "A", "B", "C", "D", "A"])
        with patch("builtins.input", side_effect=answers):
            with patch("builtins.print") as mock_print:
                result = run_understanding_check()

        self.assertEqual(result["score"], 4)
        self.assertEqual(len(result["explanations"]), 2)
        self.assertIn("score", str(mock_print.call_args_list))

    def test_grade_answers_computes_score(self):
        submitted = ["B", "C", "B", "C", "C", "B"]
        self.assertEqual(grade_answers(submitted), 4)


if __name__ == "__main__":
    unittest.main()
