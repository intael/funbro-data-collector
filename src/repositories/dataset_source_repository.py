from abc import ABC, abstractmethod
from typing import TypeVar

from src.datasets import Dataset
from src.raw_data_container import RawData

T = TypeVar("T")


class DatasetSourceRepository(ABC):
    @abstractmethod
    async def get(self, dataset: Dataset) -> RawData[T]:
        raise NotImplementedError()
