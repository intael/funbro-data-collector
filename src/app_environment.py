from enum import Enum, auto, unique


@unique
class AppEnvironment(Enum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()
