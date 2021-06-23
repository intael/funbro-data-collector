from dataclasses import dataclass
from typing import TypeVar, Generic

from src.datasets import Dataset

T = TypeVar("T")


@dataclass(frozen=True)
class RawData(Generic[T]):
    data: T
    dataset: Dataset
