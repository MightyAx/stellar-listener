from typing import List
from pathlib import Path
from sense_hat import SenseHat

from sonic_pi.tool import Server as SonicServer
from .observer import SenseHatObserver
from .transformer import OrientationTransformer
from .sounds.vega import Vega
from .sounds.polaris import Polaris
from .sounds.whitenoise import WhiteNoise

class SoundMaker:
    def __init__(self, sense: SenseHat, sonic: SonicServer, observer: SenseHatObserver):
        self.sense = sense
        self.sonic = sonic
        self.observer = observer
        self.whitenoise = WhiteNoise()
        self.signals = [Vega(), Polaris()]
        self.sounds = self.signals.copy()
        self.sounds.append(self.whitenoise)
    
    def __enter__(self):
        if self.sonic.check_if_running() != 0:
            raise RuntimeError('Sonic Pi not running')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sonic.stop_all_jobs()
        self.sense.clear()
    
    def make_sound(self):
        self.send_sounds([s.start for s in self.sounds])
        while True:
            observation = self.observer.make_observation()
            max_amp = self.observe_signals(observation)
            # ToDo: Pull the volume cap out into a config (1 amp on that whitenoise is too loud)
            self.whitenoise.apply_amplitude(1 - max_amp)
            self.send_sounds([s.sound for s in self.sounds])
    
    def observe_signals(self, observation):
        max_amp = 0
        min_sep = 180
        for signal in self.signals:
            signal.apply_observation(observation)
            # ToDo: Change this to choose one signal to highlight (prevent LED flicker)
            if signal.amplitude > max_amp:
                max_amp = signal.amplitude
            if signal.separation < min_sep:
                min_sep = signal.separation
            if (signal.separation < 10):
                self.sense.show_letter(str(signal.separation), text_colour=signal.colour)
            if min_sep > 9:
                self.sense.clear()
        return max_amp
    
    def send_sounds(self, sounds: List[str]):
        code = '\r\n'.join(sounds)
        self.sonic.run_code(code)
