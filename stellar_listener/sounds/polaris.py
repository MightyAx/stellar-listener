from .signal import BaseSignal
from stellar_listener.images.colours import Green

class Polaris(BaseSignal):
    def __init__(self):
        super().__init__('polaris', Green)
    
    def map_seperation_to_amplitude(self, seperation: int):
        if seperation < 50:
            return 1 - (seperation / 50)
        return 0
