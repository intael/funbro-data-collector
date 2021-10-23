from __future__ import annotations

from enum import Enum, unique
from typing import Type, TypeVar

from src.cli.exceptions import CLIArgumentCanNotBeParsed


@unique
class CLIParsableEnum(Enum):
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


T = TypeVar("T", bound=CLIParsableEnum, covariant=True)


def parse_cli_string_to_enum(string: str, enum_type: Type[T]) -> T:
    try:
        return enum_type[string.upper().strip()]
    except KeyError:
        raise CLIArgumentCanNotBeParsed(
            f"CLI Argument {string} can not be parsed. Valid arguments are: {set(enum_type)}"
        )
