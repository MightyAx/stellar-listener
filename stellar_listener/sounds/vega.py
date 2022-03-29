from .signal import BaseSignal


class Vega(BaseSignal):
    def __init__(self):
        super().__init__('vega', [0,0,255])
    
    def map_seperation_to_amplitude(self, seperation: int):
        if seperation < 50:
            return 1 - (seperation / 50)
        return 0
