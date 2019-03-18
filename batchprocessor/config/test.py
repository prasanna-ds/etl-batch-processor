import logging
from .default import DefaultConfig

class TestConfig(DefaultConfig):
    APP_ENV = "test"
    LOG_LEVEL = logging.DEBUG  

    S3_FILE = 'hi'
    OUTPUT_PATH = 'output/clean'