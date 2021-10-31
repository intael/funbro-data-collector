from abc import ABC, abstractmethod

from src.datasets import Dataset


class DatasetPersistenceRepository(ABC):
    @abstractmethod
    def save(self, dataset: Dataset) -> None:
        """Persists the selected dataset into a concrete storage."""
        raise NotImplementedError
