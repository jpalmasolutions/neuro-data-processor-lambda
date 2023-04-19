import json

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.batch import (BatchProcessor, EventType,
                                                   process_partial_response)
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext
from tdt import StructType

from src.main.processor import process_block
from src.main.zips3message import ZipS3Message

processor = BatchProcessor(event_type=EventType.SQS)
tracer = Tracer()
logger = Logger()


@tracer.capture_method
def record_handler(record: SQSRecord):
    payload: str = record.body
    if payload:
        item: dict = json.loads(payload)
        sns_message: dict = json.loads(item.get("Message"))
        s3_event: ZipS3Message = ZipS3Message(sns_message)
        data: StructType = s3_event.get_block_data()
        process_block(data=data)


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    return process_partial_response(
        event=event, record_handler=record_handler, processor=processor, context=context
    )
