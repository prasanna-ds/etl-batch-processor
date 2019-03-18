"""
Main app for batch processor

Usage:
    app.py --env=<env>
    app.py (-h | --help)
    app.py ( --version | -v )

Options:
  -h --help     Show this screen.
  --version     Show version.
  --env=ENV     The environment name [default: dev].

"""
from docopt import docopt, DocoptExit
from batchprocessor import VERSION
import os
import signal
from functools import partial
import sys
import boto3


DEFAULT_APP_ENV = "development"
        
if __name__ == "__main__":
        try:
            arguments = docopt(__doc__, version="etl-micro-batch-processor %s" % VERSION)
            os.environ["APP_ENV"] = arguments.get("--env", DEFAULT_APP_ENV)
        except DocoptExit:
            print("something wrong")


from batchprocessor.log import getLogger
from batchprocessor.processor import Processor 
from batchprocessor.sqs import SQSWorker
from batchprocessor.config import Config
from batchprocessor.s3notification import SQSS3Notification

LOG = getLogger("batchprocessor")
boto3.setup_default_session(region_name=Config.AWS_REGION_NAME)

def on_sqs_messages_received(sqs_messages):
    for sqs_message in sqs_messages:
        LOG.info("Received SQS Message : "+ str(sqs_message))
        notification = SQSS3Notification.from_raw(sqs_message.body)
        s3_bucket_name, s3_key = notification.s3_bucket_name, notification.s3_object_key
        if s3_bucket_name is not None and s3_key is not None:
            try:
                processor = Processor(s3_bucket_name, s3_key, output_path=Config.OUTPUT_PATH)
                processor.process()
            except:
                LOG.warning("Unable to process (%s, %s):",
                            s3_bucket_name, s3_key, exc_info=True)
            
def shutdown(worker):
    LOG.info("Shutting down worker...")
    if worker is not None and callable(getattr(worker, "stop")):
        worker.stop()
    LOG.info("done")
    sys.exit(0)

def on_signal(worker, sig, *_):
    LOG.info("Got %s", signal.Signals(sig).name) # pylint: disable=no-member
    shutdown(worker)

def start():
    LOG.info("Starting in %s", Config.APP_ENV)
    worker = None

    try:
        worker = SQSWorker(Config.SQS_QUEUE_NAME,
                    on_sqs_messages_received,
                    max_number_of_messages=Config.SQS_MAX_NUMBER_OF_MESSAGES,
                    visibility_timeout=Config.SQS_VISIBILITY_TIMEOUT,
                    wait_time_seconds=Config.SQS_WAIT_TIME_SECONDS,
                    cooldown_in_seconds=Config.SQS_WORKER_COOLDOWN_SECONDS)

        # catch signals
        signal.signal(signal.SIGINT, partial(on_signal, worker))
        
        worker.run()
    except Exception:
        LOG.exception("Shutting down due to an unhandled exception:")
        shutdown(worker)
    
if __name__ == "__main__":
    print("Starting the app..")
    start()