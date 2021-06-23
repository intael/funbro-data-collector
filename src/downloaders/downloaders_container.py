from dependency_injector import containers, providers

from src.downloaders.generic_downloader import GenericAsyncDownloader
from src.repositories.repositories_container import RepositoriesContainer
from src.serializers.serializers_container import SerializersContainer


class DownloadersContainer(containers.DeclarativeContainer):

    async_downloader: providers.Singleton = providers.Singleton(
        GenericAsyncDownloader,
        serializer=SerializersContainer.imdb_daily_serializer,
        dataset_repository=RepositoriesContainer.imdb_daily_source_repository,
    )
