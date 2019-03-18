from .log import getLogger
from .config import Config
from .extract import Extract
from .transform import Transform
from .write import Writer

LOG = getLogger(__name__)

class Processor:
    def __init__(self, s3_bucket_name, s3_key, output_path):
        self.s3_bucket_name = s3_bucket_name
        self.s3_key = s3_key
        self.output_path = output_path

        if output_path is None:
            raise AttributeError("%s arg output_path is required",
                                 self.__class__.__name__)

    def process(self):
        # extract the data from archive.
        extract = Extract(self.s3_bucket_name, self.s3_key)

        # create pandas dataframes from json data.
        transform_data = Transform(extract.load())

        # write the transformed data to S3.
        write_object = Writer(self.output_path, transform_data.transform())
        Writer.write(write_object)