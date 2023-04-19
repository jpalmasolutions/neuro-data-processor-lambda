from dataclasses import dataclass
import numpy


@dataclass
class LFPx:
    name: str
    fs: numpy.float64
    start_time: numpy.float64
    channels: list[numpy.uint16]
    data: numpy.ndarray
