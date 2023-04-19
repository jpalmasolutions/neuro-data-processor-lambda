from src.main.models.lfpx import LFPx
from src.main.models.pneu import PNEu


class Stream:
    def __init__(self, lfpx: LFPx, pneu: PNEu):
        self.lfpx = lfpx
        self.pneu = pneu
