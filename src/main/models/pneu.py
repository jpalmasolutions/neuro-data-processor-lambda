from dataclasses import dataclass
import numpy


@dataclass
class PNEu:
    data: numpy.ndarray
    name: str
    fs: numpy.float64
    start_time: numpy.float64
    code: numpy.uint32
    size: numpy.uint32
    type: numpy.uint32
    type_str: str
    ucf: numpy.bool_
    dform: numpy.uint32
    channel: list[numpy.uint16]
