import logging
import os

import psycopg2

from datasets import Dataset
from repositories.dataset_persistance_repository import DatasetPersistanceRepository
from serializers.serializers_container import SerializersContainer


class TSVFileToPostgresPersistanceRepository(DatasetPersistanceRepository):
    def __init__(self) -> None:
        self.__postgres_connection = psycopg2.connect(
            host=os.environ.get("POSTGRES_DATABASE_HOST_FIELD"),
            dbname="funbro",
            user=os.environ.get("POSTGRES_DATABASE_USER_FIELD"),
            password=os.environ.get("POSTGRES_DATABASE_PASSWORD_FIELD"),
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

    def __truncate_table(self, dataset: Dataset) -> None:
        with self.__postgres_connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE staging.{dataset.name};")
            self.__postgres_connection.commit()
