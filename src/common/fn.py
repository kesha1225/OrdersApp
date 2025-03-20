from typing import Any

from fntypes import Option, Nothing, Some, Ok, Error


def from_optional[T](value: T | None) -> Option[T]:
    return Some(value) if value is not None else Nothing()


def is_ok(some: Any) -> bool:
    return isinstance(some, Ok)


def is_err(some: Any) -> bool:
    return isinstance(some, Error)
