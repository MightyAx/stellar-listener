from .base import BaseSound
from .signal import BaseSignal


class WhiteNoise(BaseSound):
    def __init__(self): 
        super().__init__('whitenoise')
        self.max_amp = 0.5
    
    def apply_signal(self, closest_signal: BaseSignal):
        amp = (closest_signal.separation / 180) * self.max_amp
        super().apply_amplitude(amp)
