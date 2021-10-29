import logging
import sys
from argparse import Namespace
from typing import Set

from src.cli.argument_parser_factory import build_argument_parser
from src.cli.exceptions import CLIArgumentCanNotBeParsed
from src.collectors.collector_factory import CollectorFactory
from src.datasets import Dataset
from src.datasources import DataSource

format_str = "%(asctime)s [%(name)s - %(levelname)-5.5s]  %(message)s"
logging.basicConfig(
    stream=sys.stdout,
    format=format_str,
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

argument_parser = build_argument_parser()

try:
    arguments: Namespace = argument_parser.parse_args()
except CLIArgumentCanNotBeParsed as cli_error:
    logger.error(str(cli_error))
    sys.exit(1)

logger.setLevel(logging.DEBUG if arguments.debug else logging.INFO)

data_source: DataSource = DataSource[arguments.data_source]
datasets: Set[Dataset] = set(arguments.datasets)

if __name__ == "__main__":
    CollectorFactory.build_collector(data_source).collect(datasets)
