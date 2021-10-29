from dependency_injector import containers
from dependency_injector.providers import Dict, Singleton

from src.collectors.imdb_data_source_collector import ImdbDailyUpdatedDatasetCollector
from src.datasources import DataSource
from src.downloaders.downloaders_container import DownloadersContainer
from src.repositories.repositories_container import RepositoriesContainer


class CollectorsContainer(containers.DeclarativeContainer):
    collectors: Dict = Dict(
        {
            DataSource.IMDB_DAILY: Singleton(
                ImdbDailyUpdatedDatasetCollector,
                downloader=DownloadersContainer.async_downloader,
                dataset_persistence_repo_provider=RepositoriesContainer.imdb_daily_persistence_repository.provider,
            )
        }
    )
