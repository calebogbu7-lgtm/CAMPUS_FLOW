# CampusFlow Next — Baseline Check

## 1. Baseline Test Results

**Branch:** `main`

**Command:** `python3 -m unittest discover -s tests -v`

**Result:** FAILED — 25 tests ran.

- Passed: 19
- Failed: 1
- Errors: 5

## 2. Confirmed Failure

`test_invalid_urgency` failed because `calculate_priority("urgent", 5)` returned `'medium'` instead of raising `ValueError`.

## 3. Test Errors

Five tests raised `TypeError` because they supplied too few arguments to `validate_ticket_data()` or `create_ticket()`:

1. `test_boolean_affected_users`
2. `test_fractional_affected_users`
3. `test_ticket_ids_are_unique`
4. `test_ticket_structure`
5. `test_zero_affected_users`

These errors mean the tests did not successfully verify their intended behaviour.

## 4. Three Diagnostic Inputs

1. `calculate_priority("urgent", 5)`  
   **Result:** Returned `'medium'`. Invalid urgency was not rejected.

2. `calculate_priority("high", 12)`  
   **Result:** Returned `'critical'`. The valid priority calculation worked.

3. `validate_ticket_data("Test ticket", "Network", "low", True)`  
   **Result:** Raised `ValueError`. Boolean affected-user counts are rejected.

## 5. Improvements Needed

- Reject invalid urgency values in priority calculation.
- Correct the five tests that pass too few arguments.
- Verify affected-user validation using correctly formed test calls.
- Preserve existing functionality while improving validation, workflow, storage, and test coverage.

## 6. Conclusion

The original test suite is not fully passing. One failure was confirmed for invalid urgency, and five tests could not complete because of incorrect argument counts. The other 19 tests passed.

These findings establish the baseline before implementing CampusFlow Next improvements.