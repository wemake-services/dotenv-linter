import inspect
import re
from types import ModuleType

from dotenv_linter.violations.base import BaseViolation


def _get_sorted_classes(
    classes: list[BaseViolation],
) -> tuple[list[BaseViolation], list[BaseViolation]]:
    sorted_by_code = sorted(classes, key=lambda cl: cl.code)
    sorted_by_source = sorted(
        classes,
        key=lambda cl: inspect.findsource(cl)[1],
    )

    return sorted_by_code, sorted_by_source


def test_violation_source_order(
    all_module_violations: dict[ModuleType, list[BaseViolation]],
) -> None:
    """Used to force violations order inside the source code."""
    for classes in all_module_violations.values():
        sorted_by_code, sorted_by_source = _get_sorted_classes(classes)

        assert sorted_by_code == sorted_by_source


def test_violation_autoclass_order(
    all_module_violations: dict[ModuleType, list[BaseViolation]],
) -> None:
    """Used to force violations order inside the `autoclass` directives."""
    for module, classes in all_module_violations.items():
        sorted_by_code, _ = _get_sorted_classes(classes)
        pattern = re.compile(r'\.\.\sautoclass::\s(\w+)')
        sorted_by_autoclass = pattern.findall(module.__doc__)
        sorted_by_code = [cl.__qualname__ for cl in sorted_by_code]

        assert sorted_by_code == sorted_by_autoclass
