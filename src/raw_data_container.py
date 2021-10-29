from dataclasses import dataclass
from typing import Generic, TypeVar

from src.datasets import Dataset

T = TypeVar("T")


@dataclass(frozen=True)
class RawData(Generic[T]):
    data: T
    dataset: Dataset
