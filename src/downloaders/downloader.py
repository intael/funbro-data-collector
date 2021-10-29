from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.datasets import Dataset

T = TypeVar("T", bound=Dataset, covariant=True)


class Downloader(ABC, Generic[T]):
    @abstractmethod
    def download(self, datasets: set[T]) -> None:
        raise NotImplementedError()
