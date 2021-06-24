import pytest

from src.collectors.data_source_collector import DataSourceCollector
from src.datasets import ImdbDailyUpdatedDataset


def test_original_values_are_returned_without_all():
    values = {ImdbDailyUpdatedDataset.TITLE_EPISODE, ImdbDailyUpdatedDataset.TITLE_CREW}
    assert (
        DataSourceCollector.handle_cli_enums(
            set(ImdbDailyUpdatedDataset),
            values,
            ImdbDailyUpdatedDataset.ALL,
        )
        == values
    )


def test_all_values_are_returned_when_all_is_included():
    values = {ImdbDailyUpdatedDataset.ALL}
    parsed_values = list(
        DataSourceCollector.handle_cli_enums(
            set(ImdbDailyUpdatedDataset),
            values,
            ImdbDailyUpdatedDataset.ALL,
        )
    )
    all_values = list(set(ImdbDailyUpdatedDataset))
    all_values.remove(ImdbDailyUpdatedDataset.ALL)
    assert parsed_values == all_values


def test_function_throws_value_error_when_all_is_included_along_other_values():
    values = {ImdbDailyUpdatedDataset.ALL, ImdbDailyUpdatedDataset.TITLE_CREW}
    with pytest.raises(ValueError):
        DataSourceCollector.handle_cli_enums(
            set(ImdbDailyUpdatedDataset),
            values,
            ImdbDailyUpdatedDataset.ALL,
        )
