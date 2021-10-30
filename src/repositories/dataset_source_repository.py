from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.datasets import Dataset
from src.raw_data_container import RawData

T = TypeVar("T")


class DatasetSourceRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, dataset: Dataset) -> RawData[T]:
        """Retrieves a given dataset from a source."""
        raise NotImplementedError
