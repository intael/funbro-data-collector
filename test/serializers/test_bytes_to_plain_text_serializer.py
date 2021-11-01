from unittest import mock

import pytest

from src.serializers.bytes_to_plain_text_serializer import BytesToPlainTextFileSerializer


@pytest.fixture()
def open_file_to_write():
    with mock.patch("builtins.open") as _fixture:
        yield _fixture


@pytest.fixture()
def gzip_decompress():
    with mock.patch("gzip.decompress") as _fixture:
        yield _fixture


@pytest.fixture()
def serializer_instance():
    return BytesToPlainTextFileSerializer(mock.Mock())


@pytest.fixture()
def raw_data():
    raw_data = mock.Mock()
    dataset = mock.Mock()
    dataset.name = mock.Mock()
    dataset.data = mock.Mock()
    raw_data.dataset = dataset
    return raw_data


class TestBytesToPlainTextSerializer:
    def test_serialize_calls_decompress_to_expected_data(
        self, serializer_instance, open_file_to_write, raw_data, gzip_decompress
    ):
        serializer_instance.serialize(raw_data)
        gzip_decompress.assert_called_once_with(raw_data.data)

    def test_serialize_decodes_expected_data(
        self, serializer_instance, open_file_to_write, raw_data, gzip_decompress
    ):
        serializer_instance.serialize(raw_data)
        mock_decode = gzip_decompress.return_value.decode
        mock_decode.assert_called_with(encoding="utf-8")

    def test_serialize_opens_file_to_write(
        self, serializer_instance, open_file_to_write, raw_data, gzip_decompress
    ):
        serializer_instance.serialize(raw_data)
        open_file_to_write.assert_called_once()

    def test_serialize_writes_decoded_data_to_file(
        self, serializer_instance, open_file_to_write, raw_data, gzip_decompress
    ):
        serializer_instance.serialize(raw_data)
        mock_decode = gzip_decompress.return_value.decode
        mock_decode.assert_called_with(encoding="utf-8")
        open_file_to_write.return_value.__enter__.return_value.write.assert_called_once_with(
            mock_decode.return_value
        )
