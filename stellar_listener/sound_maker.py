from typing import List
from pathlib import Path
from ratelimit import limits

from sonic_pi.tool import Server as SonicServer
from .observer import SenseHatObserver
from .transformer import OrientationTransformer
from .sounds.vega import Vega
from .sounds.whitenoise import WhiteNoise

class SoundMaker:
    def __init__(self, sonic: SonicServer, observer: SenseHatObserver):
        self.sonic = sonic
        self.observer = observer
        self.vega = Vega()
        self.whitenoise = WhiteNoise()
    
    def __enter__(self):
        if self.sonic.check_if_running() != 0:
            raise RuntimeError('Sonic Pi not running')

    def __exit__(self, exc_type, exc_value, traceback):
        self.sonic.stop_all_jobs()
        self.observer.sense.clear()
    
    def make_sound(self):
        self.send_sounds([self.vega.start, self.whitenoise.start])
        while True:
            observation = self.observer.make_observation()
            self.vega.apply_observation(observation, self.observer.sense)
            self.whitenoise.apply_amplitude(1 - self.vega.amplitude)
            self.send_sounds([self.vega.sound, self.whitenoise.sound])
    
    @limits(calls=1, period=1, raise_on_limit=False)
    def send_sounds(self, sounds: List[str]):
        code = '\r\n'.join(sounds)
        self.sonic.run_code(code)
