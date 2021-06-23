from argparse import ArgumentParser

from src.datasets import ImdbDailyUpdatedDataset
from src.datasources import DataSource

DATA_SOURCE = "data_source"
DATASETS_ARGUMENT = "datasets"


def build_subparsers(parent_parser: ArgumentParser) -> ArgumentParser:
    subparsers = parent_parser.add_subparsers(
        help="Data Sources", required=True, dest=DATA_SOURCE
    )
    imdb_parser = subparsers.add_parser(
        DataSource.IMDB_DAILY.value, help="Imdb daily updated datasets collector"
    )
    imdb_parser.add_argument(
        f"--{DATASETS_ARGUMENT}",
        required=True,
        nargs="+",
        type=ImdbDailyUpdatedDataset.argparse,
        choices=set(ImdbDailyUpdatedDataset),
        help="Datasets to download",
    )
    return parent_parser
