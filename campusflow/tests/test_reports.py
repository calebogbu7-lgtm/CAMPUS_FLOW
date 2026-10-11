import unittest

from reports import generate_report


class TestReports(unittest.TestCase):

    def test_generate_report(self):
        tickets = [
            {
                "ticket_id": "T001",
                "status": "open",
                "priority": "critical",
            },
            {
                "ticket_id": "T002",
                "status": "in_progress",
                "priority": "high",
            },
            {
                "ticket_id": "T003",
                "status": "resolved",
                "priority": "medium",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total_tickets"], 3)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["medium"], 1)

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)

    def test_invalid_status(self):
        tickets = [
            {"status": "pending", "priority": "low"}
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)


if __name__ == "__main__":
    unittest.main()
