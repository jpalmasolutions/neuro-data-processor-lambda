from dataclasses import dataclass
import datetime


@dataclass
class Info:
    tankpath: str
    blockname: str
    start_date: datetime.datetime
    utc_start_time: str
    stop_date: datetime.datetime
    utc_stop_time: str
    duration: datetime.timedelta
    stream_channel: int
    snip_channel: int
