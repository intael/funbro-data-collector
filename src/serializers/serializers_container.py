from dependency_injector import containers, providers

from src.serializers.bytes_to_plain_text_serializer import BytesToPlainTextFileSerializer


class SerializersContainer(containers.DeclarativeContainer):

    STAGING_DIR_PATH = "staging"

    imdb_daily_serializer: providers.Singleton = providers.Singleton(
        BytesToPlainTextFileSerializer, file_path=STAGING_DIR_PATH
    )
