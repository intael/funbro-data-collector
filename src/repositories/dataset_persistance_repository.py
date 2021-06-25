from abc import ABC, abstractmethod

from src.datasets import Dataset


class DatasetPersistanceRepository(ABC):
    @abstractmethod
    def save(self, dataset: Dataset) -> None:
        raise NotImplementedError()
