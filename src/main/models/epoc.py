from dataclasses import dataclass

import numpy


@dataclass
class Epoc:
    name: str
    onset: numpy.ndarray
    offset: numpy.ndarray
    type: str
    type_str: str
    data: numpy.ndarray
    dform: numpy.uint32
    size: int
