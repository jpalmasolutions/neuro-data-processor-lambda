import jsons
import numpy
from tdt import StructType

from src.main.models.epoc import Epoc
from src.main.models.info import Info
from src.main.models.snip import Snip
from src.main.models.lfpx import LFPx
from src.main.models.pneu import PNEu
from src.main.models.stream import Stream


class Block:
    def __init__(self, toplevel: StructType):
        _epocs: StructType = toplevel.epocs
        _snips: StructType = toplevel.snips
        _lfpx: StructType = toplevel.streams.LFPx
        _pneu: StructType = toplevel.streams.pNeu
        _info: StructType = toplevel.info
        self.time_ranges: numpy.ndarray = toplevel.get("time_ranges")

        self.epocs: dict[str, Epoc] = dict()
        self.snips: dict[str, Snip] = dict()
        self.streams: Stream
        self.info: Info = jsons.load(_info.__dict__, Info)

        for key, val in _epocs.items():
            self.epocs[key] = jsons.load(val.__dict__, Epoc)

        for key, val in _snips.items():
            self.snips[key] = jsons.load(val.__dict__, Snip)

        lfpx = jsons.load(_lfpx.__dict__, LFPx)
        pneu = jsons.load(_pneu.__dict__, PNEu)

        self.streams = Stream(lfpx=lfpx, pneu=pneu)
