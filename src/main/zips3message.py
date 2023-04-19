import io
import shutil
import tempfile
import zipfile

import boto3
import tdt
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event
from botocore.response import StreamingBody
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef
from tdt import StructType

logger = Logger(child=True)


class ZipS3Message(S3Event):
    def __init__(self, sns_message: dict):
        super().__init__(sns_message)

    def get_block_data(self) -> StructType:
        s3: S3Client = boto3.client("s3")

        logger.info(
            msg="Retrieving Object", bucket=self.bucket_name, object=self.object_key
        )

        object_response: GetObjectOutputTypeDef = s3.get_object(
            Bucket=self.bucket_name, Key=self.object_key
        )

        object_stream: StreamingBody = object_response["Body"]
        object_data: bytes = object_stream.read()

        temp_dir_path: str = tempfile.mkdtemp()

        with io.BytesIO(object_data) as object_bytes:
            # Read the file as a zipfile and process the members
            with zipfile.ZipFile(object_bytes, mode="r") as zip_file:
                logger.info(temp_dir_path)
                zip_file.extractall(path=temp_dir_path)

        data: StructType = tdt.read_block(block_path=temp_dir_path, sortname="TankSort")
        shutil.rmtree(path=temp_dir_path)

        return data
