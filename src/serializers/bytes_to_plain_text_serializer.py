import gzip

from src.raw_data_container import RawData, T
from src.serializers.serializer import Serializer


class BytesToPlainTextFileSerializer(Serializer):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def serialize(self, raw_data: RawData[T]) -> None:
        with open(f"{self.__file_path}/{raw_data.dataset.name}.tsv", "w") as file:
            file.write(gzip.decompress(raw_data.data).decode(encoding="utf-8"))
