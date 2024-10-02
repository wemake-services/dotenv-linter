import inspect
from collections.abc import Callable
from operator import itemgetter
from pathlib import PurePath
from types import ModuleType
from typing import Dict, List

import pytest
from typing_extensions import TypeAlias

from dotenv_linter import violations
from dotenv_linter.violations.base import (
    BaseFileViolation,
    BaseFSTViolation,
    BaseViolation,
)

ALL_VIOLATIONS_TYPE: TypeAlias = Dict[ModuleType, List[BaseViolation]]


def _is_violation_class(cls) -> bool:
    base_classes = {
        BaseViolation,
        BaseFSTViolation,
        BaseFileViolation,
    }
    if not inspect.isclass(cls):
        return False

    return issubclass(cls, BaseViolation) and cls not in base_classes


def _load_all_violation_classes() -> ALL_VIOLATIONS_TYPE:
    modules = [
        violations.assigns,
        violations.comments,
        violations.names,
        violations.parsing,
        violations.values,
    ]

    classes = {}
    for module in modules:
        classes_names_list = inspect.getmembers(module, _is_violation_class)
        only_classes = map(itemgetter(1), classes_names_list)
        classes.update({module: list(only_classes)})
    return classes


@pytest.fixture(scope='session')
def all_violations() -> List[BaseViolation]:
    """Loads all violations from the package."""
    classes = _load_all_violation_classes()
    all_errors_container = []
    for module_classes in classes.values():
        all_errors_container.extend(module_classes)
    return all_errors_container


@pytest.fixture(scope='session')
def all_module_violations() -> ALL_VIOLATIONS_TYPE:
    """Loads all violations from the package."""
    return _load_all_violation_classes()


@pytest.fixture()
def fixture_path() -> Callable[[str], str]:
    """Returns path to the fixture."""
    def factory(path: str) -> str:
        return str(PurePath(__file__).parent.joinpath('fixtures', path))
    return factory


@pytest.fixture(scope='session')
def all_violation_codes(
    all_module_violations: ALL_VIOLATIONS_TYPE,  # noqa: WPS442
) -> Dict[ModuleType, Dict[int, BaseViolation]]:
    """Loads all codes and their violation classes from the package."""
    return {
        module: {
            violation.code: violation
            for violation in all_module_violations[module]
        }
        for module in all_module_violations.keys()
    }
