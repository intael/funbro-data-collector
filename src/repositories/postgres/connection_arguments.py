from typing import Optional

from pydantic import BaseSettings, Field, validator

from src.app_environment import AppEnvironment

ENVIRON_KEY = "environment"


class PostgresConnectionArguments(BaseSettings):
    environment: AppEnvironment = Field(env="ENVIRONMENT")
    host: str = Field(env="POSTGRES_DATABASE_HOST_FIELD")
    dbname: str = Field(env="POSTGRES_DATABASE_NAME")
    user: str = Field(env="POSTGRES_DATABASE_USER_FIELD")
    port: str = Field(env="POSTGRES_DATABASE_PORT_FIELD")
    password: str = Field(env="POSTGRES_DATABASE_PASSWORD_FIELD")
    sslmode: str = Field(env="POSTGRES_SSL_MODE")
    sslcert: Optional[str] = Field(env="POSTGRES_DATABASE_CLIENT_CERT_PATH")
    sslkey: Optional[str] = Field(env="POSTGRES_DATABASE_CLIENT_KEY_PATH")
    sslrootcert: Optional[str] = Field(env="POSTGRES_DATABASE_SERVER_CA_PATH")

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"

    @validator(ENVIRON_KEY, pre=True)
    def validate_environment(cls, v: str) -> AppEnvironment:
        try:
            return AppEnvironment[v.upper()]
        except KeyError:
            raise ValueError(f"Invalid environment, it should be one of {list(AppEnvironment)}")

    @validator("sslmode")
    def validate_sslmode(cls, v: str, values: dict[str, str]) -> str:
        if (values[ENVIRON_KEY] == AppEnvironment.PRODUCTION and v != "require") or (
            values[ENVIRON_KEY] == AppEnvironment.DEVELOPMENT and v != "disable"
        ):
            raise ValueError(
                "The sslmode argument should be 'require' when the environment is production and 'disable' when the environment is development."
            )
        return v

    @validator("sslcert", "sslkey", "sslrootcert")
    def validate_ssl_credentials(
        cls, v: Optional[str], values: dict[str, str], field: str
    ) -> Optional[str]:
        if values[ENVIRON_KEY] == AppEnvironment.PRODUCTION and not v:
            raise ValueError(
                f"The {field} argument was found to be null with Environment=production."
            )
        return v
