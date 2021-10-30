from multiprocessing.pool import Pool
from unittest import mock

import pytest
from pytest_mock import MockerFixture

from src.collectors.data_source_collector import DataSourceCollector
from src.collectors.imdb_data_source_collector import ImdbDailyUpdatedDatasetCollector
from src.datasets import ImdbDailyUpdatedDataset


@pytest.fixture
def imdb_daily_updated_dataset_collector(mocker: MockerFixture):
    downloader, persistence_repo_provider = mocker.Mock(), mocker.Mock()
    return ImdbDailyUpdatedDatasetCollector(downloader, persistence_repo_provider)


@pytest.fixture()
def multiprocess_pool_apply_fixture():
    with mock.patch.object(Pool, "starmap", return_value=None) as _fixture:
        yield _fixture


@pytest.fixture(scope="module")
def persist_collected_datasets_fixture():
    with mock.patch(
        "src.collectors.imdb_data_source_collector._persist_collected_datasets",
        return_value=None,
    ) as _fixture:
        yield _fixture


@pytest.fixture()
def handle_cli_args_fixture():
    with mock.patch.object(DataSourceCollector, "handle_cli_enums") as _fixture:
        yield _fixture


class TestImdbDailyUpdatedDatasetCollector:
    @pytest.mark.parametrize(
        "datasets",
        [
            {ImdbDailyUpdatedDataset.TITLE_RATINGS},
            {
                ImdbDailyUpdatedDataset.NAME_BASICS,
                ImdbDailyUpdatedDataset.TITLE_AKAS,
            },
            {
                ImdbDailyUpdatedDataset.TITLE_RATINGS,
                ImdbDailyUpdatedDataset.TITLE_CREW,
                ImdbDailyUpdatedDataset.TITLE_PRINCIPALS,
            },
        ],
    )
    def test_collect_calls_handle_cli_enums_with_the_right_args(
        self,
        imdb_daily_updated_dataset_collector: ImdbDailyUpdatedDatasetCollector,
        datasets: set[ImdbDailyUpdatedDataset],
        handle_cli_args_fixture,
        multiprocess_pool_apply_fixture,
    ):
        handle_cli_args_fixture.return_value = datasets
        imdb_daily_updated_dataset_collector.collect(datasets)
        handle_cli_args_fixture.assert_called_once_with(
            set(ImdbDailyUpdatedDataset), datasets, ImdbDailyUpdatedDataset.ALL
        )

    def test_collect_calls_handle_cli_enums_with_all_and_all_get_downloaded(
        self, mocker: MockerFixture, multiprocess_pool_apply_fixture
    ):
        downloader = mocker.Mock()
        downloader.download = mocker.Mock(return_value=None)
        collector = ImdbDailyUpdatedDatasetCollector(downloader, mocker.Mock())
        all_datasets = {ImdbDailyUpdatedDataset.ALL}
        collector.collect(all_datasets)
        all_values = set(ImdbDailyUpdatedDataset)
        all_values.remove(ImdbDailyUpdatedDataset.ALL)
        downloader.download.assert_called_with(all_values)

    def test_collect_errors_when_called_with_empty_datasets(
        self,
        imdb_daily_updated_dataset_collector: ImdbDailyUpdatedDatasetCollector,
    ):
        with pytest.raises(ValueError):
            imdb_daily_updated_dataset_collector.collect(set())

    def test_collect_calls_multiprocess_pool_properly(
        self,
        mocker: MockerFixture,
        handle_cli_args_fixture,
        persist_collected_datasets_fixture,
        multiprocess_pool_apply_fixture,
    ):
        datasets = {
            ImdbDailyUpdatedDataset.NAME_BASICS,
            ImdbDailyUpdatedDataset.TITLE_AKAS,
        }
        persistence_repo_provider = mocker.Mock()
        collector = ImdbDailyUpdatedDatasetCollector(mocker.Mock(), persistence_repo_provider)
        handle_cli_args_fixture.return_value = datasets
        collector.collect(datasets)
        multiprocess_pool_apply_fixture.assert_called_once_with(
            func=persist_collected_datasets_fixture,
            iterable={(dataset, persistence_repo_provider) for dataset in datasets},
        )

    def test_collect_calls_downloaders_download_method_with_the_right_arg(
        self,
        mocker: MockerFixture,
        handle_cli_args_fixture,
        multiprocess_pool_apply_fixture,
    ):
        datasets = {
            ImdbDailyUpdatedDataset.NAME_BASICS,
            ImdbDailyUpdatedDataset.TITLE_AKAS,
        }
        downloader = mocker.Mock()
        handle_cli_args_fixture.return_value = datasets
        downloader.download = mocker.Mock(return_value=None)
        collector = ImdbDailyUpdatedDatasetCollector(downloader, mocker.Mock())
        collector.collect(datasets)
        downloader.download.assert_called_once_with(datasets)
