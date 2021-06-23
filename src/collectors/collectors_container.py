from dependency_injector import containers, providers

from collectors.imdb_data_source_collector import ImdbDailyUpdatedDatasetCollector
from datasources import DataSource
from downloaders.downloaders_container import DownloadersContainer
from repositories.repositories_container import RepositoriesContainer


class CollectorsContainer(containers.DeclarativeContainer):

    collectors = providers.Dict(
        {
            DataSource.IMDB_DAILY: providers.Singleton(
                ImdbDailyUpdatedDatasetCollector,
                downloader=DownloadersContainer.async_downloader,
                dataset_persistence_repo_provider=RepositoriesContainer.imdb_daily_persistence_repository.provider,
            )
        }
    )
