import os

from .development import DevelopmentConfig
from .production import ProductionConfig
from .test import TestConfig

DEFAULT_APP_ENV = "development"

if os.environ.get("APP_ENV",DEFAULT_APP_ENV) == "production":
    Config = ProductionConfig
elif os.environ.get("APP_ENV",DEFAULT_APP_ENV) == "development":
    Config = DevelopmentConfig
elif os.environ.get("APP_ENV",DEFAULT_APP_ENV) == "test":
    Config = TestConfig