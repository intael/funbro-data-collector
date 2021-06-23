from abc import ABC, abstractmethod
from typing import TypeVar

from datasets import Dataset
from raw_data_container import RawData

T = TypeVar("T")


class DatasetSourceRepository(ABC):
    @abstractmethod
    async def get(self, dataset: Dataset) -> RawData[T]:
        raise NotImplementedError()
