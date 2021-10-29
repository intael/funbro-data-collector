from dependency_injector import containers, providers

from serializers.serializer import Serializer
from src.serializers.bytes_to_plain_text_serializer import BytesToPlainTextFileSerializer


class SerializersContainer(containers.DeclarativeContainer):
    STAGING_DIR_PATH: str = "staging"

    imdb_daily_serializer: providers.Singleton[Serializer[bytes]] = providers.Singleton(
        BytesToPlainTextFileSerializer, file_path=STAGING_DIR_PATH
    )
