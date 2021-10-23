import argparse
import functools
from argparse import ArgumentParser

from cli.cli_parsable import parse_cli_string_to_enum
from src.datasets import ImdbDailyUpdatedDataset
from src.datasources import DataSource

DATA_SOURCE = "data_source"
DATASETS_ARGUMENT = "datasets"
DEBUG_FLAG = "debug"


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Funbro Data Collector",
        description="Downloads raw data used by the Funbro app.",
    )
    parser.add_argument(
        f"--{DEBUG_FLAG}",
        action="store_true",
        default=False,
        help="Enable debug-level logs.",
    )
    _attach_datasource_subparser(parser)
    return parser


def _attach_datasource_subparser(
    parent_parser: ArgumentParser,
) -> None:
    data_source_subparser = parent_parser.add_subparsers(
        help="Data Sources", required=True, dest=DATA_SOURCE
    )
    imdb_parser = data_source_subparser.add_parser(
        DataSource.IMDB_DAILY.value, help="Imdb daily updated datasets collector"
    )

    imdb_parser.add_argument(
        f"--{DATASETS_ARGUMENT}",
        required=True,
        nargs="+",
        type=functools.partial(
            parse_cli_string_to_enum, enum_type=ImdbDailyUpdatedDataset
        ),
        choices=set(ImdbDailyUpdatedDataset),
        help="Datasets to download",
    )
