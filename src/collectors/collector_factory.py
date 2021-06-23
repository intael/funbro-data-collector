from src.collectors.collectors_container import CollectorsContainer
from src.collectors.data_source_collector import DataSourceCollector
from src.datasources import DataSource


class CollectorFactory:
    @staticmethod
    def build_collector(data_source: DataSource) -> DataSourceCollector:
        return CollectorsContainer.collectors.kwargs[data_source]()
