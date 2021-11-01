from test.conftest import DATASETS_FIXTURE
from unittest import mock

import pytest

from src.datasets import Dataset
from src.repositories.async_raw_dataset_source_repository import AsyncRawDatasetSourceRepository


@pytest.fixture()
def get_response():
    return mock.Mock()


@pytest.fixture()
def async_get(get_response):
    return mock.AsyncMock(return_value=get_response)


@pytest.fixture()
def async_http_client(async_get):
    client = mock.Mock()
    client.get = async_get
    return client


@pytest.fixture()
def dataset_source_repo_instance(async_http_client):
    return AsyncRawDatasetSourceRepository(async_http_client)


class TestAsyncRawDatasetSourceRepository:
    @pytest.mark.parametrize(
        "dataset",
        DATASETS_FIXTURE,
    )
    @pytest.mark.asyncio
    async def test_request_is_awaited_with_a_given_dataset(
        self, dataset: Dataset, dataset_source_repo_instance, async_get, get_response
    ):
        await dataset_source_repo_instance.get(dataset)
        async_get.assert_awaited_once_with(dataset.value)

    @pytest.mark.parametrize(
        "dataset",
        DATASETS_FIXTURE,
    )
    @pytest.mark.asyncio
    async def test_response_is_checked_for_status(
        self, dataset: Dataset, dataset_source_repo_instance, get_response
    ):
        await dataset_source_repo_instance.get(dataset)
        get_response.raise_for_status.assert_called_once()

    @pytest.mark.parametrize(
        "dataset",
        DATASETS_FIXTURE,
    )
    @pytest.mark.asyncio
    async def test_response_matches_expectation(
        self, dataset: Dataset, dataset_source_repo_instance, get_response
    ):
        response = await dataset_source_repo_instance.get(dataset)
        assert get_response.content == response.data

    @pytest.mark.parametrize(
        "dataset",
        DATASETS_FIXTURE,
    )
    @pytest.mark.asyncio
    async def test_returned_rawdata_dataset_matches_expectation(
        self, dataset: Dataset, dataset_source_repo_instance
    ):
        response = await dataset_source_repo_instance.get(dataset)
        assert dataset == response.dataset
