from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.datasets import Dataset

T = TypeVar("T", bound=Dataset, covariant=True)


class Downloader(ABC, Generic[T]):
    @abstractmethod
    def download(self, datasets: set[T]) -> None:
        """Handles the download of a number of datasets, normally (but not necessarily) delegating the responsibility
        of fetching the data to a repository"""
        raise NotImplementedError
