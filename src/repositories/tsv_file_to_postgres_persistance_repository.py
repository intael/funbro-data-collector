import logging
import os

import psycopg2

from src.datasets import Dataset
from src.repositories.dataset_persistance_repository import DatasetPersistanceRepository
from src.serializers.serializers_container import SerializersContainer


class TSVFileToPostgresPersistanceRepository(DatasetPersistanceRepository):
    def __init__(self) -> None:
        connection_arguments = dict(
            host=os.environ.get("POSTGRES_DATABASE_HOST_FIELD"),
            dbname=os.environ.get("POSTGRES_DATABASE_NAME"),
            user=os.environ.get("POSTGRES_DATABASE_USER_FIELD"),
            password=os.environ.get("POSTGRES_DATABASE_PASSWORD_FIELD"),
        )
        if os.environ.get("ENVIRONMENT", "development") == "production":
            connection_arguments.update(
                **dict(
                    sslmode="require",
                    sslcert=os.environ.get("POSTGRES_DATABASE_CLIENT_CERT_PATH"),
                    sslkey=os.environ.get("POSTGRES_DATABASE_CLIENT_KEY_PATH"),
                    sslrootcert=os.environ.get("POSTGRES_DATABASE_SERVER_CA_PATH"),
                )
            )
        self.__postgres_connection = psycopg2.connect(**connection_arguments)
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
