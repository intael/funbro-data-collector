from abc import ABC, abstractmethod
from typing import Set, TypeVar, Generic

from src.datasets import Dataset

T = TypeVar("T", bound=Dataset, covariant=True)

class AsyncDownloader(ABC, Generic[T]):
    @abstractmethod
    async def download(self, datasets: Set[T]) -> None:
        raise NotImplementedError()
