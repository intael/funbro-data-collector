from abc import ABC, abstractmethod
from typing import Set

from datasets import Dataset


class AsyncDonwloader(ABC):
    @abstractmethod
    async def download(self, datasets: Set[Dataset]) -> None:
        raise NotImplementedError()
