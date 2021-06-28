from pydantic import BaseSettings, Field, validator

from src.environment import Environment


class PostgresConnectionArguments(BaseSettings):

    environment: Environment = Field(env="ENVIRONMENT", default=Environment.DEVELOPMENT)
    host: str = Field(env="POSTGRES_DATABASE_HOST_FIELD")
    dbname: str = Field(env="POSTGRES_DATABASE_NAME")
    user: str = Field(env="POSTGRES_DATABASE_USER_FIELD")
    password: str = Field(env="POSTGRES_DATABASE_PASSWORD_FIELD")
    sslmode: str = Field(env="POSTGRES_SSL_MODE")
    sslcert: str = Field(env="POSTGRES_DATABASE_CLIENT_CERT_PATH")
    sslkey: str = Field(env="POSTGRES_DATABASE_CLIENT_KEY_PATH")
    sslrootcert: str = Field(env="POSTGRES_DATABASE_SERVER_CA_PATH")

    @validator("environment")
    def validate_environment(cls, v):
        print(v, isinstance(v, Environment))
        envs = [value for value in Environment]
        if not isinstance(v, Environment):
            raise ValueError(f"Invalid environment, it should be one of {envs}")
        return v

    @validator("sslmode")
    def validate_sslmode(cls, v, values):
        print(values)
        if (values["environment"] == Environment.PRODUCTION and v != "require") or (
            values["environment"] == Environment.DEVELOPMENT and v != "disable"
        ):
            raise ValueError(
                "The sslmode argument should be 'require' when the environment is production and 'disable' when the environment is development."
            )

    @validator("sslcert")
    def validate_sslcert(cls, v, values):
        if values["environment"] == Environment.PRODUCTION and not v:
            raise ValueError(
                "The sslcert argument was found to be null with Environemnt=production."
            )
        return v

    @validator("sslkey")
    def validate_sslkey(cls, v, values):
        if values["environment"] == Environment.PRODUCTION and not v:
            raise ValueError(
                "The sslkey argument was found to be null with Environemnt=production."
            )
        return v

    @validator("sslrootcert")
    def validate_sslrootcert(cls, v, values):
        if values["environment"] == Environment.PRODUCTION and not v:
            raise ValueError(
                "The sslrootcert argument was found to be null with Environemnt=production."
            )
        return v
