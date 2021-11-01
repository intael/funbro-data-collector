import pytest

from src.datasets import ImdbDailyUpdatedDataset

DATASETS_FIXTURE = {
    dataset for dataset in set(ImdbDailyUpdatedDataset) if dataset != ImdbDailyUpdatedDataset.ALL
}


@pytest.fixture()
def all_imdb_datasets():
    return {
        dataset
        for dataset in set(ImdbDailyUpdatedDataset)
        if dataset != ImdbDailyUpdatedDataset.ALL
    }
