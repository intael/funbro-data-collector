from dependency_injector import containers, providers
from httpx import AsyncClient

from repositories.dataset_persistance_repository import DatasetPersistenceRepository
from repositories.dataset_source_repository import DatasetSourceRepository
from src.repositories.imdb_daily_updated_dataset_repository import (
    ImdbDailyUpdatedDatasetSourceRepository,
)
from src.repositories.postgres.connection_arguments import PostgresConnectionArguments
from src.repositories.tsv_file_to_postgres_persistance_repository import (
    TSVFileToPostgresPersistenceRepository,
)


class RepositoriesContainer(containers.DeclarativeContainer):
    postgres_conn_args = providers.Singleton(
        PostgresConnectionArguments,
    )

    http_client = providers.Singleton(AsyncClient, timeout=60)

    imdb_daily_source_repository: providers.Singleton[
        DatasetSourceRepository[bytes]
    ] = providers.Singleton(ImdbDailyUpdatedDatasetSourceRepository, http_client=http_client)

    imdb_daily_persistence_repository: providers.Factory[
        DatasetPersistenceRepository
    ] = providers.Factory(
        TSVFileToPostgresPersistenceRepository,
        postgres_connection_arguments=postgres_conn_args,
    )
