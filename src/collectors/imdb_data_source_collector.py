import multiprocessing
from multiprocessing import Pool

from dependency_injector.providers import Provider

from src.collectors.data_source_collector import DataSourceCollector
from src.datasets import Dataset, ImdbDailyUpdatedDataset
from src.downloaders.downloader import Downloader
from src.repositories.dataset_persistance_repository import DatasetPersistenceRepository


def _persist_collected_datasets(
    dataset: Dataset,
    dataset_persistence_repo_provider: Provider[DatasetPersistenceRepository],
) -> None:
    dataset_persistence_repo_provider().save(dataset)


class ImdbDailyUpdatedDatasetCollector(DataSourceCollector[ImdbDailyUpdatedDataset]):
    def __init__(
        self,
        downloader: Downloader,
        dataset_persistence_repo_provider: Provider[DatasetPersistenceRepository],
    ):
        """
        dataset_persistence_repo_provider is a provider because we need to instantiate it
        inside the python process that runs it, otherwise Python complains about serializing
        a mutable object.
        :param dataset_persistence_repo_provider:
        """
        self.__dataset_persistence_repo_provider = dataset_persistence_repo_provider
        self.__downloader = downloader

    def collect(self, datasets: set[ImdbDailyUpdatedDataset]) -> None:
        if len(datasets) == 0:
            raise ValueError(
                "Collector was asked to collect an empty set of datasets. At least one is required."
            )
        parsed_dataset_enums: set[ImdbDailyUpdatedDataset] = self.handle_cli_enums(
            set(ImdbDailyUpdatedDataset), datasets, ImdbDailyUpdatedDataset.ALL
        )  # this parsing of the datasets enum is done here because other collectors might not need to do this parsing
        self.__downloader.download(parsed_dataset_enums)
        usable_cores: int = min(multiprocessing.cpu_count() - 1, len(parsed_dataset_enums))
        with Pool(usable_cores) as process_pool:
            process_pool.starmap(
                func=_persist_collected_datasets,
                iterable={
                    (dataset, self.__dataset_persistence_repo_provider)
                    for dataset in parsed_dataset_enums
                },
            )
