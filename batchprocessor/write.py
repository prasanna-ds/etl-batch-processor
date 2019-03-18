import boto3
import gzip
from io import BytesIO, TextIOWrapper
import datetime
from urllib.parse import urlparse

from .log import getLogger
from .config import Config

LOG = getLogger(__name__)

class Writer(object):
    def __init__(self, output_path, transformed_data):
        self.s3_path = output_path
        self.transformed_data = transformed_data
        s3Session = boto3.Session(
                        region_name=Config.AWS_REGION_NAME,
                        aws_access_key_id=Config.ACCESS_KEY,
                        aws_secret_access_key=Config.SECRET_ACCESS_KEY,
                )

        self.s3 = s3Session.resource("s3")

    def write(self):

        #fs = s3fs.S3FileSystem(key=Config.ACCESS_KEY, secret=Config.SECRET_ACCESS_KEY)

        for table in self.transformed_data:
            if table is not None:
                try:
                    buffer = BytesIO()

                    with gzip.GzipFile(mode='w', fileobj=buffer) as zipped_file:
                        table.to_csv(TextIOWrapper(zipped_file, 'utf8'), index=False)
                
                    now = datetime.datetime.now()
                        
                    s3_url = self.s3_path + '/' + now.strftime("%Y-%m-%d") + '/' + str(now.hour) + '/' + table.name + '.csv.gz'
                    LOG.info("Writing table %s as %s", table.name, s3_url)
                    s3_path_refined= urlparse(s3_url)

                    s3_object = self.s3.Object(s3_path_refined.netloc, s3_path_refined.path.replace('/', '', 1))
                    s3_object.put(Body=buffer.getvalue())
                except Exception as e:
                    LOG.error(e)
