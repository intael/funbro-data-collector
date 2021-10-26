from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from typeguard import typechecked

from src.datasets import Dataset

T = TypeVar("T", bound=Dataset, covariant=True)


class DataSourceCollector(ABC, Generic[T]):
    @abstractmethod
    def collect(self, datasets: set[T]) -> None:
        raise NotImplementedError()

    @classmethod
    @typechecked
    def handle_cli_enums(
        cls,
        all_constant_values: set[T],
        chosen_constant_values: set[T],
        all_constant: Dataset,
    ) -> set[T]:
        if len(chosen_constant_values) > 1 and all_constant in chosen_constant_values:
            raise ValueError(
                f"The 'ALL' token has been chosen for the dimension {type(all_constant).__name__}, but it is not the"
                f" only one. Choose either ALL or a few from this list: {set(type(all_constant))}"
            )
        elif all_constant in chosen_constant_values:
            return {value for value in all_constant_values if value != all_constant}
        else:
            return chosen_constant_values
