from asyncio import as_completed
from typing import Set, List
from collections.abc import Coroutine

from src.datasets import Dataset
from src.downloaders.downloader import AsyncDownloader
from src.raw_data_container import RawData
from src.repositories.dataset_source_repository import DatasetSourceRepository
from src.serializers.serializer import Serializer


class GenericAsyncDownloader(AsyncDownloader):
    def __init__(
        self,
        dataset_repository: DatasetSourceRepository,
        serializer: Serializer,
    ):
        self.__dataset_repository = dataset_repository
        self.__serializer = serializer

    async def download(self, datasets: Set[Dataset]) -> None:
        awaitables: List[Coroutine] = [
            self.__dataset_repository.get(dataset) for dataset in datasets
        ]
        for result in as_completed(awaitables):
            raw_data: RawData[bytes] = await result
            self.__serializer.serialize(raw_data)
