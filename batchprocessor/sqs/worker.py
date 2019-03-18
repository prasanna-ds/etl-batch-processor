import boto3
from ..log import getLogger
from time import sleep
from batchprocessor.config import Config

LOG = getLogger(__name__)

DEFAULT_MAX_NUMBER_OF_MESSAGES = 1
DEFAULT_VISIBILITY_TIMEOUT = 120
DEFAULT_WAIT_TIME_SECONDS = 20
DEFAULT_COOLDOWN_IN_SECONDS = 10

class SQSWorker:
    def __init__(self, queue_name, on_messages_received,         # pylint: disable=too-many-arguments
                 max_number_of_messages=DEFAULT_MAX_NUMBER_OF_MESSAGES,
                 visibility_timeout=DEFAULT_VISIBILITY_TIMEOUT,
                 wait_time_seconds=DEFAULT_WAIT_TIME_SECONDS,
                 cooldown_in_seconds=DEFAULT_COOLDOWN_IN_SECONDS):
        if queue_name is None:
            raise AttributeError("Required %s arg 'queue_name' is missing" % self.__class__.__name__)

        self.queue_name = queue_name
        self.on_messages_received = on_messages_received
        self.max_number_of_messages = max_number_of_messages
        self.visibility_timeout = visibility_timeout
        self.wait_time_seconds = wait_time_seconds
        self.cooldown_in_seconds = cooldown_in_seconds

        # ACCESS KEY and SECRET KEY. This is not a best practice in any production environment to embed the keys
        # and the best practice is to use IAM role.
        session = boto3.Session(
                        region_name=Config.AWS_REGION_NAME,
                        aws_access_key_id=Config.ACCESS_KEY,
                        aws_secret_access_key=Config.SECRET_ACCESS_KEY,
                )

        self.sqs = session.resource("sqs")
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

        self.shutting_down = False

    def run(self):
        LOG.debug("Running...")
        while not self.shutting_down:
            self.on_messages_received(self.__receive_messages())
            if self.cooldown_in_seconds > 0:
                LOG.info("Sleeping for %d seconds...", self.cooldown_in_seconds)
                sleep(self.cooldown_in_seconds)

    def stop(self):
        LOG.debug("Stopping...")
        self.shutting_down = True

    def __receive_messages(self):
        LOG.info("Looking for work in SQS...")
        try:
            return self.queue.receive_messages(
                MaxNumberOfMessages=self.max_number_of_messages,
                VisibilityTimeout=self.visibility_timeout,
                WaitTimeSeconds=self.wait_time_seconds,
            )
        except KeyError:
            LOG.warning("Ignored KeyError when looking for messages in SQS:", exc_info=True)
            return []