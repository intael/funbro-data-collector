import gzip

from raw_data_container import RawData
from serializers.serializer import Serializer


class BytesToPlainTextFileSerializer(Serializer):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def serialize(self, bytes_data: RawData[bytes]) -> None:
        with open(f"{self.__file_path}/{bytes_data.dataset.name}.tsv", "w") as file:
            file.write(gzip.decompress(bytes_data.data).decode(encoding="utf-8"))
