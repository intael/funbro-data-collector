import asyncio
from asyncio import as_completed
from collections.abc import Coroutine

from src.datasets import Dataset
from src.downloaders.downloader import Downloader
from src.repositories.dataset_source_repository import DatasetSourceRepository
from src.serializers.serializer import Serializer


class AsyncDownloader(Downloader[Dataset]):
    def __init__(
        self,
        dataset_repository: DatasetSourceRepository,
        serializer: Serializer,
    ):
        self.__dataset_repository = dataset_repository
        self.__serializer = serializer

    def download(self, datasets: set[Dataset]) -> None:
        coroutines: list[Coroutine] = [
            self.__dataset_repository.get(dataset) for dataset in datasets
        ]
        asyncio.run(self.__run_download_coroutines(coroutines))

    async def __run_download_coroutines(self, coroutines: list[Coroutine]) -> None:
        for result in as_completed(coroutines):
            self.__serializer.serialize(await result)
