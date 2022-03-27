from .base import BaseSoundCoord

class Vega(BaseSoundCoord):
    def __init__(self):
        super().__init__('vega', [0,0,255])
    
    def map_seperation_to_amplitute(self, seperation: int):
        return seperation / 180
    