from abc import ABC, abstractmethod
from typing import Set, Optional, TypeVar

from typeguard import typechecked

from src.cli.cli_parsable import CLIParsableEnum
from src.datasets import Dataset

T = TypeVar("T", bound=CLIParsableEnum)


class DataSourceCollector(ABC):
    @abstractmethod
    def collect(self, datasets: Set[Dataset]) -> None:
        raise NotImplementedError()

    @classmethod
    @typechecked
    def handle_cli_enums(
        cls,
        all_constant_values: Set[T],
        chosen_constant_values: Set[T],
        all_constant: Optional[T] = None,
    ) -> Optional[Set[T]]:
        if (
            all_constant
            and len(chosen_constant_values) > 1
            and all_constant in chosen_constant_values
        ):
            raise ValueError(
                f"The 'ALL' token has been chosen for the dimension {type(all_constant).__name__}, but it is not the only one. Choose either ALL or a few from this list: {set(type(all_constant))}"
            )
        elif not all_constant and all_constant in chosen_constant_values:
            raise ValueError(
                f"The 'ALL' token has been chosen for the dimension {type(all_constant).__name__}, but it has not been included in the call ('all_constant' argument)."
            )
        elif all_constant and all_constant in chosen_constant_values:
            all_constant_values.remove(all_constant)
            return all_constant_values
        else:
            return chosen_constant_values
