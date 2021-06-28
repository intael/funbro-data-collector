import argparse
import logging
import os
import shutil
import stat
import sys
from typing import Dict, Any, Set

from files_util import FilesUtil
from src.cli.exceptions import CLIArgumentCanNotBeParsed
from src.cli.subparsers import build_subparsers, DATA_SOURCE, DATASETS_ARGUMENT
from src.collectors.collector_factory import CollectorFactory
from src.collectors.collectors_container import CollectorsContainer
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

if os.environ.get("ENVIRONMENT", "development") == "production":
    FilesUtil.copy_dir_files(".credentials", "staging", [".gitkeep"])
    FilesUtil.change_dir_files_permissions("staging", [".gitkeep"])

data_source: DataSource = DataSource[arguments[DATA_SOURCE]]
datasets: Set[Dataset] = set(arguments[DATASETS_ARGUMENT])


if __name__ == "__main__":
    collector: DataSourceCollector = CollectorFactory.build_collector(data_source)
    collector.collect(datasets)
    for file in {file for file in os.listdir("staging") if file != ".gitkeep"}:
        FilesUtil.remove_dir_files("staging", [".gitkeep"])
