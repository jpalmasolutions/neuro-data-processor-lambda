from dataclasses import dataclass

import numpy


@dataclass
class Snip:
    name: str
    code: numpy.uint32
    size: numpy.uint32
    type: numpy.uint32
    type_str: str
    fs: numpy.float64
    dform: numpy.uint32
    ts: numpy.ndarray
    data: numpy.ndarray
    chan: numpy.ndarray
    sortcode: numpy.ndarray
    sortname: str
