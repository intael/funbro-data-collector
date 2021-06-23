from dependency_injector import containers, providers
from httpx import AsyncClient

from repositories.imdb_daily_updated_dataset_repository import (
    ImdbDailyUpdatedDatasetSourceRepository,
)
from repositories.tsv_file_to_postgres_persistance_repository import (
    TSVFileToPostgresPersistanceRepository,
)


class RepositoriesContainer(containers.DeclarativeContainer):

    http_client = providers.Singleton(AsyncClient, timeout=60)

    imdb_daily_source_repository: providers.Singleton = providers.Singleton(
        ImdbDailyUpdatedDatasetSourceRepository, http_client=http_client
    )

    imdb_daily_persistence_repository: providers.Factory = providers.Factory(
        TSVFileToPostgresPersistanceRepository
    )
