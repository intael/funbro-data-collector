from unittest import mock

import pytest

from src.datasets import ImdbDailyUpdatedDataset
from src.repositories.postgres.connection_arguments import ENVIRON_KEY
from src.repositories.tsv_file_to_postgres_persistance_repository import (
    TSVFileToPostgresPersistenceRepository,
)


@pytest.fixture()
def postgres_connection():
    with mock.patch("psycopg2.connect") as _fixture:
        yield _fixture


@pytest.fixture()
def postgres_cursor(postgres_connection):
    mock_cursor = mock.MagicMock()
    postgres_connection.return_value.cursor.return_value = mock_cursor
    return mock_cursor


@pytest.fixture()
def postgres_cursor_execute(postgres_cursor):
    return postgres_cursor.__enter__.return_value.execute


@pytest.fixture()
def postgres_cursor_copy_expert(postgres_cursor):
    return postgres_cursor.__enter__.return_value.copy_expert


@pytest.fixture()
def open_file():
    with mock.patch("builtins.open", mock.mock_open(read_data="data")) as _fixture:
        yield _fixture


@pytest.fixture()
def remove_file():
    with mock.patch("os.remove", return_value=None) as _fixture:
        yield _fixture


@pytest.fixture()
def postgres_args_dict_fixture():
    with mock.patch.dict({}, values={ENVIRON_KEY: "foobar"}, clear=True) as _fixture:
        yield _fixture


@pytest.fixture()
def postgres_args(postgres_args_dict_fixture):
    postgres_args = mock.Mock()
    postgres_args.dict = mock.Mock(return_value=postgres_args_dict_fixture)
    return postgres_args


@pytest.fixture()
def repo_instance(postgres_args):
    return TSVFileToPostgresPersistenceRepository(postgres_args)


class TestTsvFileToPostgresPersistenceRepository:
    def test_removes_environment_key_from_dict_at_instantiation(
        self, postgres_args, postgres_connection, postgres_args_dict_fixture
    ):
        TSVFileToPostgresPersistenceRepository(postgres_args)
        postgres_args.dict.assert_called_once()
        postgres_connection.assert_called_once_with(**postgres_args_dict_fixture)

    def test_truncate_is_executed_with_right_query(
        self,
        postgres_connection,
        postgres_cursor,
        postgres_cursor_execute,
        postgres_cursor_copy_expert,
        postgres_args,
        open_file,
        remove_file,
        repo_instance,
    ):
        dataset = ImdbDailyUpdatedDataset.TITLE_RATINGS
        repo_instance.save(dataset)
        postgres_cursor_execute.assert_called_with(f"TRUNCATE staging.{dataset.name};")

    def test_copy_is_executed_with_right_query_and_file(
        self,
        postgres_connection,
        postgres_cursor,
        postgres_cursor_execute,
        postgres_cursor_copy_expert,
        postgres_args,
        open_file,
        remove_file,
        repo_instance,
    ):
        dataset = ImdbDailyUpdatedDataset.TITLE_RATINGS
        repo_instance.save(dataset)
        postgres_cursor_copy_expert.assert_called_with(
            sql=f"COPY staging.{dataset.name} FROM STDIN DELIMITER AS '\t'",
            file=open_file.return_value,
        )

    def test_queries_are_commited_expected_times(
        self,
        postgres_connection,
        postgres_cursor,
        postgres_cursor_execute,
        postgres_cursor_copy_expert,
        postgres_args,
        open_file,
        remove_file,
        repo_instance,
    ):
        repo_instance.save(ImdbDailyUpdatedDataset.TITLE_RATINGS)
        postgres_connection.return_value.commit.assert_has_calls([mock.call(), mock.call()])

    def test_connection_is_closed(
        self,
        postgres_connection,
        postgres_cursor,
        postgres_cursor_execute,
        postgres_cursor_copy_expert,
        postgres_args,
        open_file,
        remove_file,
        repo_instance,
    ):
        repo_instance.save(ImdbDailyUpdatedDataset.TITLE_RATINGS)
        postgres_connection.return_value.close.assert_called_once()
