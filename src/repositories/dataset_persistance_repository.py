from abc import ABC, abstractmethod

from src.datasets import Dataset


class DatasetPersistanceRepository(ABC):
    @abstractmethod
    async def save(self, dataset: Dataset) -> None:
        raise NotImplementedError()
