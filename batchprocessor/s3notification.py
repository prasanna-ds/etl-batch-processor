import datetime
import json
import urllib

from .log import getLogger

LOG = getLogger(__name__)

class SQSS3Notification:
    @staticmethod
    def from_raw(raw_message_body):
        return SQSS3Notification(*_parse(raw_message_body))

    def __init__(self, s3_bucket_name, s3_object_key):
        self.s3_bucket_name = s3_bucket_name
        self.s3_object_key = s3_object_key
                
def _parse(raw_message_body):
    sqs_message = json.loads(raw_message_body)
    LOG.info("SQS Message Received: %s", sqs_message)

    try:
        payload = json.loads(sqs_message["Message"]) 
    except:
        payload = sqs_message# yes, it's a json inside a json

    _s3_notifications = payload.get("Records", [])
    if len(_s3_notifications) <= 0:
        LOG.warning("SQS Message without any records: %s", payload)
        return (None, None)

    s3_notification = _s3_notifications[0]
    s3_bucket_name = s3_notification.get("s3", {}).get("bucket", {}).get("name", None)
    s3_object_key = s3_notification.get("s3", {}).get("object", {}).get("key", None)

    if "%3D" in s3_object_key:
        s3_object_key = urllib.parse.unquote(s3_object_key)

    if s3_bucket_name is None or s3_object_key is None:
        LOG.warning("S3 notification missing either bucket or key: bucket=%s, key=%s",
                    s3_bucket_name, s3_object_key)
    return (s3_bucket_name, s3_object_key)
