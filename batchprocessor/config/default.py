import logging

class DefaultConfig():
    AWS_REGION_NAME = 'ap-southeast-1'
    LOG_LEVEL = logging.DEBUG
    
    # Queue name
    SQS_QUEUE_NAME = 'CDSSummaryToParquetConversion'

    # Number of messages to be received 
    SQS_MAX_NUMBER_OF_MESSAGES = 10
    
    # How long a message needs to be hidden from other consumers while being processed
    SQS_VISIBILITY_TIMEOUT = 600

    # Long polling. this is the max value 
    SQS_WAIT_TIME_SECONDS = 20

    # Frequency of making SQS requests
    SQS_WORKER_COOLDOWN_SECONDS = 600

    # ACCESS KEY and SECRET KEY. This is not a best practice in any production environment to embed the keys
    # and the best practice is to use IAM role.
    ACCESS_KEY = ''
    SECRET_ACCESS_KEY = ''  

    S3_FILE = ''
    OUTPUT_PATH = ''
