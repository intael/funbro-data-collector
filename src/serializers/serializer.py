from abc import ABC, abstractmethod

from raw_data_container import RawData, T


class Serializer(ABC):
    @abstractmethod
    def serialize(self, bytes_data: RawData[T]) -> None:
        raise NotImplementedError()
