from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    UAT = "uat"
    LOCAL = "local"
    PROD = "prod"
