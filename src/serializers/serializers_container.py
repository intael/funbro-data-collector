from pathlib import Path

from dependency_injector import containers, providers

from src.serializers.bytes_to_plain_text_serializer import BytesToPlainTextFileSerializer
from src.serializers.serializer import Serializer


class SerializersContainer(containers.DeclarativeContainer):
    STAGING_DIR_PATH: Path = Path("staging")

    imdb_daily_serializer: providers.Singleton[Serializer[bytes]] = providers.Singleton(
        BytesToPlainTextFileSerializer, directory_path=STAGING_DIR_PATH
    )
