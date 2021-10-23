import logging
import sys
from typing import Any, Dict, Set

from cli.argument_parser_factory import (
    DATA_SOURCE,
    DATASETS_ARGUMENT,
    DEBUG_FLAG,
    build_argument_parser,
)
from src.cli.exceptions import CLIArgumentCanNotBeParsed
from src.collectors.collector_factory import CollectorFactory
from src.collectors.data_source_collector import DataSourceCollector
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
    arguments: Dict[str, Any] = vars(argument_parser.parse_args())
except CLIArgumentCanNotBeParsed as cli_error:
    logger.error(str(cli_error))
    sys.exit(1)

logger.setLevel(logging.DEBUG if arguments[DEBUG_FLAG] else logging.INFO)

data_source: DataSource = DataSource[arguments[DATA_SOURCE]]
datasets: Set[Dataset] = set(arguments[DATASETS_ARGUMENT])


if __name__ == "__main__":
    collector: DataSourceCollector = CollectorFactory.build_collector(data_source)
    collector.collect(datasets)
