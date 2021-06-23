import argparse
import logging
import sys
from typing import Dict, Any, Set


from cli.exceptions import CLIArgumentCanNotBeParsed
from cli.subparsers import build_subparsers, DATA_SOURCE, DATASETS_ARGUMENT
from collector_runner import run_collector
from collectors.collectors_container import CollectorsContainer
from datasets import Dataset
from datasources import DataSource
from repositories.repositories_container import RepositoriesContainer
from serializers.serializers_container import SerializersContainer

format_str = "%(asctime)s [%(name)s - %(levelname)-5.5s]  %(message)s"
logging.basicConfig(
    stream=sys.stdout,
    format=format_str,
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog="Funbro Data Collector",
    description="Downloads raw data used by the Funbro app.",
)

parser.add_argument(
    f"--debug",
    action="store_true",
    default=False,
    help="Enable debug-level logs.",
)

parser = build_subparsers(parser)
try:
    arguments: Dict[str, Any] = vars(parser.parse_args())
except CLIArgumentCanNotBeParsed as cli_error:
    logger.error(str(cli_error))
    sys.exit(1)

logger.setLevel(logging.DEBUG if arguments["debug"] else logging.INFO)

data_source: DataSource = DataSource[arguments[DATA_SOURCE]]
datasets: Set[Dataset] = set(arguments[DATASETS_ARGUMENT])


if __name__ == "__main__":
    container = CollectorsContainer()
    container.wire(
        modules=[
            sys.modules[__name__]
        ]
    )

    run_collector(data_source, datasets)
