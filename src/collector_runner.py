from typing import Set

from dependency_injector import providers
from dependency_injector.wiring import inject, Provider

from collectors.collectors_container import CollectorsContainer
from datasets import Dataset
from datasources import DataSource


@inject
def run_collector(
    data_source: DataSource,
    datasets: Set[Dataset],
    collectors_provider: providers.Dict = Provider[CollectorsContainer.collectors],
) -> None:
    collectors_provider.kwargs[data_source]().collect(datasets)
