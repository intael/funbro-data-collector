import asyncio
import logging

from httpx import AsyncClient
from typeguard import typechecked

from src.raw_data_container import RawData
from src.datasets import Dataset
from src.repositories.dataset_source_repository import DatasetSourceRepository, T


class ImdbDailyUpdatedDatasetSourceRepository(DatasetSourceRepository):
    @typechecked
    def __init__(self, http_client: AsyncClient):
        self.__http_client = http_client
        self.__logger = logging.getLogger(self.__class__.__name__)

    async def get(self, dataset: Dataset) -> RawData[T]:
        self.__logger.info(f"Downloading dataset {dataset.name}...")
        response = await self.__http_client.get(dataset.value)
        response.raise_for_status()
        self.__logger.info(f"Done downloading dataset: {dataset.name}.")
        return RawData(response.content, dataset)
