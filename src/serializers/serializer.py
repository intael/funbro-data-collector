from abc import ABC, abstractmethod
from typing import Generic

from src.raw_data_container import RawData, T


class Serializer(ABC, Generic[T]):
    @abstractmethod
    def serialize(self, raw_data: RawData[T]) -> None:
        raise NotImplementedError()
