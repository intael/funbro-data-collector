import gzip
import logging

from src.raw_data_container import RawData
from src.serializers.serializer import Serializer


class BytesToPlainTextFileSerializer(Serializer[bytes]):
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__logger = logging.getLogger(self.__class__.__name__)

    def serialize(self, raw_data: RawData[bytes]) -> None:
        with open(f"{self.__file_path}/{raw_data.dataset.name}.tsv", "w") as file:
            self.__logger.info(f"Writing dataset {raw_data.dataset.name} to disk.")
            file.write(gzip.decompress(raw_data.data).decode(encoding="utf-8"))
