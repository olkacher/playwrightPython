from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeAlias

from playwright.sync_api import Locator, expect

Check: TypeAlias = Callable[[], None]


def check_visible(name: str, locator: Locator) -> Check:
    def _check() -> None:
        try:
            expect(locator).to_be_visible()
        except AssertionError as exc:
            raise AssertionError(f"{name}: should be visible\n{exc}") from exc
    return _check


def check_enabled(name: str, locator: Locator) -> Check:
    def _check() -> None:
        try:
            expect(locator).to_be_enabled()
        except AssertionError as exc:
            raise AssertionError(f"{name}: should be enabled\n{exc}") from exc
    return _check


def check_text(name: str, locator: Locator, expected_text: str) -> Check:
    def _check() -> None:
        try:
            expect(locator).to_have_text(expected_text)
        except AssertionError as exc:
            raise AssertionError(
                f"{name}: should have exact text '{expected_text}'\n{exc}"
            ) from exc
    return _check


def check_contains_text(name: str, locator: Locator, expected_text: str) -> Check:
    def _check() -> None:
        try:
            expect(locator).to_contain_text(expected_text)
        except AssertionError as exc:
            raise AssertionError(
                f"{name}: should contain text '{expected_text}'\n{exc}"
            ) from exc
    return _check


def check_not_empty(name: str, locator: Locator) -> Check:
    def _check() -> None:
        try:
            actual_text = locator.text_content()
            if actual_text is None or not actual_text.strip():
                raise AssertionError(f"{name}: should not be empty")
        except AssertionError:
            raise
        except Exception as exc:
            raise AssertionError(f"{name}: failed to read text\n{exc}") from exc
    return _check


def assert_all(checks: Iterable[Check]) -> None:
    errors: list[str] = []

    for check in checks:
        try:
            check()
        except AssertionError as exc:
            errors.append(str(exc))

    if errors:
        joined = "\n\n".join(f"{index}. {error}" for index, error in enumerate(errors, start=1))
        raise AssertionError(f"Multiple UI checks failed:\n\n{joined}")