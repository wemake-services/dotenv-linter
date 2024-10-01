from collections import Counter
from typing import Dict, List

from dotenv_linter.violations.base import BaseViolation


def test_all_unique_violation_codes(
    all_violations: List[BaseViolation],
) -> None:
    """Ensures that all violations have unique violation codes."""
    codes = [int(violation.code) for violation in all_violations]

    assert len(set(codes)) == len(all_violations)


def test_all_violations_are_final(all_violations: List[BaseViolation]) -> None:
    """Ensures that all violations are final."""
    for violation_type in all_violations:
        assert getattr(violation_type, '__final__', False), violation_type


def test_all_unique_violation_messages(
    all_violations: List[BaseViolation],
) -> None:
    """Ensures that all violations have unique violation messages."""
    messages = Counter([
        violation.error_template for violation in all_violations
    ])
    for message, count in messages.items():
        assert count == 1, message


def test_no_holes(all_violation_codes: Dict) -> None:
    """Ensures that there are no off-by-one errors."""
    for module_codes in all_violation_codes.values():
        previous_code = None
        for code in sorted(module_codes.keys()):
            if previous_code is not None:
                diff = code - previous_code
                assert diff == 1 or diff > 2, module_codes[code].__qualname__
            previous_code = code
