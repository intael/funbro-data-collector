import asyncio
import multiprocessing
from functools import partial
from multiprocessing import Pool
from typing import Set

from dependency_injector.wiring import Provider

from collectors.data_source_collector import DataSourceCollector
from datasets import Dataset
from downloaders.downloader import AsyncDonwloader
from repositories.dataset_persistance_repository import DatasetPersistanceRepository


def _persist_collected_datasets(
    dataset: Dataset,
    dataset_persistence_repo_provider: Provider[DatasetPersistanceRepository],
) -> None:
    dataset_persistence_repo_provider().save(dataset)


class ImdbDailyUpdatedDatasetCollector(DataSourceCollector):
    def __init__(
        self,
        downloader: AsyncDonwloader,
        dataset_persistence_repo_provider: Provider[DatasetPersistanceRepository],
    ):
        """
        dataset_persistence_repo_provider is a provider because we need to instantiate it
        inside the python process that runs it, otherwise Python complains about serializing
        a mutable object.
        :param dataset_persistence_repo_provider:
        """
        self.__dataset_persistence_repo_provider = dataset_persistence_repo_provider
        self.__downloader = downloader

    def collect(self, datasets: Set[Dataset]) -> None:
        parsed_dataset_enums: Set[Dataset] = self.handle_cli_enums(
            set(type(list(datasets)[0])), datasets, type(list(datasets)[0]).ALL
        )
        asyncio.run(self.__downloader.download(parsed_dataset_enums))
        usable_cores: int = min(
            multiprocessing.cpu_count() - 1, len(parsed_dataset_enums)
        )
        with Pool(usable_cores) as process_pool:
            process_pool.map(
                partial(
                    _persist_collected_datasets,
                    dataset_persistence_repo_provider=self.__dataset_persistence_repo_provider,
                ),
                datasets,
            )