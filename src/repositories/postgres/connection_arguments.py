from typing import Optional

from pydantic import BaseSettings, Field, validator

from src.environment import Environment


class PostgresConnectionArguments(BaseSettings):

    environment: Environment = Field(env="ENVIRONMENT")
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

    @validator("environment", pre=True)
    def validate_environment(cls, v):
        envs = [value for value in Environment]
        if not isinstance(Environment[v.upper()], Environment):
            raise ValueError(f"Invalid environment, it should be one of {envs}")
        return Environment[v.upper()]

    @validator("sslmode")
    def validate_sslmode(cls, v, values):
        if (values["environment"] == Environment.PRODUCTION and v != "require") or (
            values["environment"] == Environment.DEVELOPMENT and v != "disable"
        ):
            raise ValueError(
                "The sslmode argument should be 'require' when the environment is production and 'disable' when the environment is development."
            )
        return v

    @validator("sslcert")
    def validate_sslcert(cls, v, values):
        if values["environment"] == Environment.PRODUCTION and not v:
            raise ValueError(
                "The sslcert argument was found to be null with Environment=production."
            )
        return v

    @validator("sslkey")
    def validate_sslkey(cls, v, values):
        if values["environment"] == Environment.PRODUCTION and not v:
            raise ValueError(
                "The sslkey argument was found to be null with Environment=production."
            )
        return v

    @validator("sslrootcert")
    def validate_sslrootcert(cls, v, values):
        if values["environment"] == Environment.PRODUCTION and not v:
            raise ValueError(
                "The sslrootcert argument was found to be null with Environment=production."
            )
        return v
