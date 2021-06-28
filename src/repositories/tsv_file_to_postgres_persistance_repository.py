import logging
import os

import psycopg2

from src.repositories.postgres.connection_arguments import PostgresConnectionArguments
from src.datasets import Dataset
from src.repositories.dataset_persistance_repository import DatasetPersistanceRepository
from src.serializers.serializers_container import SerializersContainer


class TSVFileToPostgresPersistanceRepository(DatasetPersistanceRepository):
    def __init__(
        self, postgres_connection_arguments: PostgresConnectionArguments
    ) -> None:
        self.__postgres_connection = psycopg2.connect(
            **postgres_connection_arguments.dict()
        )
        self.__logger = logging.getLogger(self.__class__.__name__)

    def save(self, dataset: Dataset) -> None:
        file_path: str = (
            os.path.join(".", SerializersContainer.STAGING_DIR_PATH, dataset.name)
            + ".tsv"
        )
        self.__logger.info(f"Truncating staging.{dataset.name} table.")
        self.__truncate_table(dataset)
        self.__logger.info(f"Loading {dataset.name} into Postgres instance.")
        with open(file_path, "r") as file:
            next(file)  # skipping header row
            with self.__postgres_connection.cursor() as cursor:
                cursor.copy_expert(
                    sql=f"COPY staging.{dataset.name} FROM STDIN DELIMITER AS '\t'",
                    file=file,
                )
                self.__postgres_connection.commit()
        self.__postgres_connection.close()
        os.remove(file_path)

    def __truncate_table(self, dataset: Dataset) -> None:
        with self.__postgres_connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE staging.{dataset.name};")
            self.__postgres_connection.commit()
