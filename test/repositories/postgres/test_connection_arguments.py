import pytest

from src.app_environment import AppEnvironment
from src.repositories.postgres.connection_arguments import ENVIRON_KEY, PostgresConnectionArguments


@pytest.mark.parametrize("environment", [AppEnvironment.PRODUCTION, AppEnvironment.DEVELOPMENT])
def test_validate_environment_happy_path(environment: AppEnvironment):
    assert PostgresConnectionArguments.validate_environment(environment.name) == environment


def test_validate_environment_errors_when_value_is_invalid():
    with pytest.raises(ValueError):
        PostgresConnectionArguments.validate_environment("wololooo")


@pytest.mark.parametrize(
    "value,environment",
    [
        ("require", AppEnvironment.PRODUCTION),
        ("disable", AppEnvironment.DEVELOPMENT),
    ],
)
def test_validate_sslmode_happy_path(value: str, environment: AppEnvironment):
    values = {ENVIRON_KEY: environment}
    assert PostgresConnectionArguments.validate_sslmode(value, values) == value


@pytest.mark.parametrize(
    "value,environment",
    [
        ("disable", AppEnvironment.PRODUCTION),
        ("require", AppEnvironment.DEVELOPMENT),
    ],
)
def test_validate_sslmode_errors_when_environ_and_value_combo_is_invalid(
    value: str, environment: AppEnvironment
):
    values = {ENVIRON_KEY: environment}
    with pytest.raises(ValueError):
        PostgresConnectionArguments.validate_sslmode(value, values)


@pytest.mark.parametrize(
    "value,environment,field",
    [
        ("foo", AppEnvironment.PRODUCTION, "sslcert"),
        ("foo", AppEnvironment.PRODUCTION, "sslkey"),
        ("foo", AppEnvironment.PRODUCTION, "sslrootcert"),
        ("foo", AppEnvironment.DEVELOPMENT, "sslrootcert"),
        (None, AppEnvironment.DEVELOPMENT, "sslrootcert"),
    ],
)
def test_validate_ssl_credentials_happy_path(value, environment, field):
    values = {ENVIRON_KEY: environment}
    PostgresConnectionArguments.validate_ssl_credentials(value, values, field)


@pytest.mark.parametrize(
    "value,environment,field",
    [
        (None, AppEnvironment.PRODUCTION, "sslcert"),
        (None, AppEnvironment.PRODUCTION, "sslkey"),
        (None, AppEnvironment.PRODUCTION, "sslrootcert"),
    ],
)
def test_validate_ssl_credentials_errors_when_value_is_null_in_production(
    value, environment, field
):
    values = {ENVIRON_KEY: environment}
    with pytest.raises(ValueError):
        PostgresConnectionArguments.validate_ssl_credentials(value, values, field)
