from asyncio import as_completed
from typing import Set

from datasets import Dataset
from downloaders.downloader import AsyncDonwloader
from repositories.dataset_source_repository import DatasetSourceRepository
from serializers.serializer import Serializer


class GenericAsyncDownloader(AsyncDonwloader):
    def __init__(
        self,
        dataset_repository: DatasetSourceRepository,
        serializer: Serializer,
    ):
        self.__dataset_repository = dataset_repository
        self.__serializer = serializer

    async def download(self, datasets: Set[Dataset]) -> None:
        awaitables = [self.__dataset_repository.get(dataset) for dataset in datasets]
        for result in as_completed(awaitables):
            raw_data = await result
            self.__serializer.serialize(raw_data)
