from enum import auto, unique, Enum


@unique
class Environment(Enum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()
