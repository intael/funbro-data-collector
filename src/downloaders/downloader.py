from abc import ABC, abstractmethod
from typing import Set

from src.datasets import Dataset


class AsyncDownloader(ABC):
    @abstractmethod
    async def download(self, datasets: Set[Dataset]) -> None:
        raise NotImplementedError()
