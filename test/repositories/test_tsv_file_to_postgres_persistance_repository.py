from unittest import mock

import pytest

from src.repositories.postgres.connection_arguments import ENVIRON_KEY
from src.repositories.tsv_file_to_postgres_persistance_repository import (
    TSVFileToPostgresPersistanceRepository,
)


@pytest.fixture(scope="module")
def postgres_connect():
    with mock.patch(
        "psycopg2.connect",
        return_value=None,
    ) as _fixture:
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


class TestTsvFileToPostgresPersistanceRepository:
    def test_removes_environment_key_from_dict_at_instantiation(
        self, postgres_args, postgres_connect, postgres_args_dict_fixture
    ):
        TSVFileToPostgresPersistanceRepository(postgres_args)
        postgres_args.dict.assert_called_once()
        postgres_connect.assert_called_once_with(**postgres_args_dict_fixture)
