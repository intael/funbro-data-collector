from enum import Enum, auto, unique


@unique
class Environment(Enum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()
