import pytest

from src.cli.cli_parsable import parse_cli_string_to_enum
from src.cli.exceptions import CLIArgumentCanNotBeParsed
from src.datasets import ImdbDailyUpdatedDataset


class TestParseCLIStringToEnum:
    @pytest.mark.parametrize(
        "cli_string,enum_value",
        [(enum_value.name, enum_value) for enum_value in list(ImdbDailyUpdatedDataset)],
    )
    def test_parse_cli_string_to_enum_happy_path(
        self, cli_string: str, enum_value: ImdbDailyUpdatedDataset
    ):
        assert parse_cli_string_to_enum(cli_string, ImdbDailyUpdatedDataset) == enum_value

    def test_parse_cli_string_errors_when_passed_invalid_string(self):
        with pytest.raises(CLIArgumentCanNotBeParsed):
            parse_cli_string_to_enum("chicks with dicks", ImdbDailyUpdatedDataset)
