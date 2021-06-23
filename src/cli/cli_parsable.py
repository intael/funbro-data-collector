from enum import unique, Enum

from typeguard import typechecked

from src.cli.exceptions import CLIArgumentCanNotBeParsed


@unique
class CLIParsableEnum(Enum):
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    @typechecked
    def argparse(cls, string: str) -> "CLIParsableEnum":
        try:
            return cls[string.upper().strip()]
        except KeyError:
            raise CLIArgumentCanNotBeParsed(
                f"CLI Argument {string} can not be parsed. Valid arguments are: {set(cls)}"
            )
