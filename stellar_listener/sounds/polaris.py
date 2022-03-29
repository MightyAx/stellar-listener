from .signal import BaseSignal


class Polaris(BaseSignal):
    def __init__(self):
        super().__init__('polaris', [0,255,0])
    
    def map_seperation_to_amplitute(self, seperation: int):
        if seperation < 50:
            return 1 - (seperation / 50)
        return 0
