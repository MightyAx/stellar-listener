from .signal import BaseSignal

class Polaris(BaseSignal):
    def __init__(self):
        super().__init__('polaris', blue=True)
    
    def map_seperation_to_amplitude(self, seperation: int):
        if seperation < 50:
            return 1 - (seperation / 50)
        return 0
