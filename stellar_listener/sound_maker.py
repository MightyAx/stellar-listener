from typing import List
from pathlib import Path
from sense_hat import SenseHat

from sonic_pi.tool import Server as SonicServer
from .observer import SenseHatObserver
from .transformer import OrientationTransformer
from .joystick import JoystickHandler
from .sounds.signal import BaseSignal
from .sounds.vega import Vega
from .sounds.polaris import Polaris
from .sounds.whitenoise import WhiteNoise

class SoundMaker:
    def __init__(self, sense: SenseHat, sonic: SonicServer, observer: SenseHatObserver, joystick: JoystickHandler):
        self.sense = sense
        self.sonic = sonic
        self.observer = observer
        self.joystick = joystick
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
            self.observe_signals(observation)
            self.whitenoise.apply_signal(self.signals[0])
            self.send_sounds([s.sound for s in self.sounds])
            print(self.signals[0].name + ', ' + str(self.signals[0].separation))
            if not self.joystick.handle_events():
                self.show_display(self.signals[0])
    
    def observe_signals(self, observation):
        for signal in self.signals:
            signal.apply_observation(observation)
        self.signals.sort(key=lambda signal: signal.separation)
    
    def send_sounds(self, sounds: List[str]):
        code = '\r\n'.join(sounds)
        self.sonic.run_code(code)

    def show_display(self, closest_signal: BaseSignal):
        if closest_signal.separation < 10:
            self.sense.show_letter(str(closest_signal.separation), text_colour=closest_signal.colour)
        else:
            self.sense.clear()
