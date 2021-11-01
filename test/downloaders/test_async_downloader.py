from test.conftest import DATASETS_FIXTURE
from unittest import mock

import pytest

from src.downloaders.async_downloader import AsyncDownloader


@pytest.fixture()
def dataset_source_repo():
    repo_get = mock.AsyncMock()
    repo = mock.Mock()
    repo.get = repo_get
    return repo


@pytest.fixture()
def serializer():
    serializer = mock.Mock()
    serializer.serialize = mock.Mock()
    return mock.Mock()


@pytest.fixture()
def downloader_instance(dataset_source_repo, serializer):
    return AsyncDownloader(dataset_repository=dataset_source_repo, serializer=serializer)


class TestAsyncDownloader:
    def test_downloads_are_awaited(self, downloader_instance, dataset_source_repo):
        downloader_instance.download(DATASETS_FIXTURE)
        dataset_source_repo.get.assert_has_awaits(
            [mock.call(dataset) for dataset in DATASETS_FIXTURE], any_order=True
        )

    def test_downloaded_datasets_are_serialized(
        self, downloader_instance, dataset_source_repo, serializer
    ):
        downloader_instance.download(DATASETS_FIXTURE)
        serializer.serialize.assert_has_calls(
            [mock.call(dataset_source_repo.get.return_value) for _ in DATASETS_FIXTURE]
        )
