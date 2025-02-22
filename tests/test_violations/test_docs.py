from types import ModuleType

from dotenv_linter.violations.base import BaseViolation


def test_all_violations_are_documented(
    all_module_violations: dict[ModuleType, list[BaseViolation]],
) -> None:
    """Ensures that all violations are documented."""
    for module, classes in all_module_violations.items():
        for violation_class in classes:
            # Once per `autoclass`
            assert module.__doc__.count(violation_class.__qualname__) == 1


def test_all_violations_have_versionadded(
    all_violations: list[BaseViolation],
) -> None:
    """Ensures that all violations have `versionadded` tag."""
    for violation in all_violations:
        assert '.. versionadded:: ' in violation.__doc__


def test_violation_name(all_violations: list[BaseViolation]) -> None:
    """Ensures that all violations have `Violation` suffix."""
    for violation in all_violations:
        class_name = violation.__qualname__
        assert class_name.endswith('Violation'), class_name


def test_violation_template_ending(all_violations: list[BaseViolation]) -> None:
    """Ensures that all violation templates do not end with a dot."""
    for violation in all_violations:
        assert not violation.error_template.endswith('.'), violation


def test_previous_codes_versionchanged(
    all_violations: list[BaseViolation],
) -> None:
    """Tests that we put both in case violation changes."""
    for violation in all_violations:
        previous_codes = getattr(violation, 'previous_codes', None)
        if previous_codes is not None:
            assert violation.__doc__.count(
                '.. versionchanged::',
            ) >= len(violation.previous_codes)
