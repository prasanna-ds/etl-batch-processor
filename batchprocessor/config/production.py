import logging
from .default import DefaultConfig

class ProductionConfig(DefaultConfig):
    APP_ENV = "production"
    LOG_LEVEL = logging.INFO

    # Number of messages to be received 
    SQS_MAX_NUMBER_OF_MESSAGES = 10
    
    # How long a message needs to be hidden from other consumers while being processed
    SQS_VISIBILITY_TIMEOUT = 600

    # Long polling. this is the max value 
    SQS_WAIT_TIME_SECONDS = 20

    # Frequency of making SQS requests
    SQS_WORKER_COOLDOWN_SECONDS = 30

    # ACCESS KEY and SECRET KEY. This is not a best practice in any production environment to embed the keys
    # and the best practice is to use IAM role.
    ACCESS_KEY = ''
    SECRET_ACCESS_KEY = ''

    OUTPUT_PATH = ''
