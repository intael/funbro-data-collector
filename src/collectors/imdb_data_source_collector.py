import asyncio
import multiprocessing
from functools import partial
from multiprocessing import Pool
from typing import Set

from dependency_injector.wiring import Provider

from src.collectors.data_source_collector import DataSourceCollector
from src.datasets import Dataset, ImdbDailyUpdatedDataset
from src.downloaders.downloader import AsyncDownloader


def _persist_collected_datasets(
    dataset: Dataset,
    dataset_persistence_repo_provider: Provider,
) -> None:
    dataset_persistence_repo_provider().save(dataset)


class ImdbDailyUpdatedDatasetCollector(DataSourceCollector[ImdbDailyUpdatedDataset]):
    def __init__(
        self,
        downloader: AsyncDownloader,
        dataset_persistence_repo_provider: Provider,
    ):
        """
        dataset_persistence_repo_provider is a provider because we need to instantiate it
        inside the python process that runs it, otherwise Python complains about serializing
        a mutable object.
        :param dataset_persistence_repo_provider:
        """
        self.__dataset_persistence_repo_provider = dataset_persistence_repo_provider
        self.__downloader = downloader

    def collect(self, datasets: Set[ImdbDailyUpdatedDataset]) -> None:
        parsed_dataset_enums: Set[ImdbDailyUpdatedDataset] = self.handle_cli_enums(
            set(ImdbDailyUpdatedDataset), datasets, ImdbDailyUpdatedDataset.ALL
        )  # this parsing of the datasets enum is done here because other collectors might not need to do this parsing
        asyncio.run(self.__downloader.download(parsed_dataset_enums))
        usable_cores: int = min(multiprocessing.cpu_count() - 1, len(parsed_dataset_enums))
        with Pool(usable_cores) as process_pool:
            process_pool.map(
                partial(
                    _persist_collected_datasets,
                    dataset_persistence_repo_provider=self.__dataset_persistence_repo_provider,
                ),
                parsed_dataset_enums,
            )
