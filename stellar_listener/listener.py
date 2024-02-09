from typing import List
from pathlib import Path

from .output.audio import Audio
from .output.display import Display
from .input.gyroscope import Gyroscope
from .input.joystick import Joystick

from .output.sounds.signal import BaseSignal
from .output.sounds.vega import Vega
from .output.sounds.polaris import Polaris
from .output.sounds.whitenoise import WhiteNoise
from .output.images.bulb import bulb_off, bulb_on
from .output.images.speaker import speaker_down, speaker_up

class Listener:
    def __init__(self, display: Display, audio: Audio, gyroscope: Gyroscope, joystick: Joystick):
        self.display = display
        self.audio = audio
        self.gyroscope = gyroscope
        self.joystick = joystick
        self.joystick.callback_up = self.button_up
        self.joystick.callback_down = self.button_down
        self.joystick.callback_left = self.button_left
        self.joystick.callback_right = self.button_right
        
        self.whitenoise = WhiteNoise()
        self.signals = [Vega(), Polaris()]
        self.audio.sounds = self.signals.copy()
        self.audio.sounds.append(self.whitenoise)
    
    def __enter__(self):
        if self.audio.sonic.check_if_running() != 0:
            raise RuntimeError('Sonic Pi not running')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.audio.sonic.stop_all_jobs()
        self.display.clear()
    
    def listen(self):
        self.audio.init_sounds()
        while True:
            self.detect_rotation()
            self.audio.send_sounds()
            if not self.joystick.handle_events():
                self.show_closest(self.signals[0])
    
    def detect_rotation(self):
        observation = self.gyroscope.make_observation()
        for signal in self.signals:
            signal.apply_observation(observation)
        self.signals.sort(key=lambda signal: signal.separation)
        self.whitenoise.apply_signal(self.signals[0])

    def show_closest(self, closest_signal: BaseSignal):
        if closest_signal.separation < 10:
            self.display.letter(str(closest_signal.separation), closest_signal.red, closest_signal.green, closest_signal.blue)
        else:
            self.display.clear()
    
    def button_up(self):
        self.display.brightness_up()
        self.display.image(bulb_on)

    def button_down(self):
        self.display.brightness_down()
        self.display.image(bulb_off)

    def button_left(self):
        self.audio.volume_down()
        self.display.image(speaker_down)

    def button_right(self):
        self.audio.volume_up()
        self.display.image(speaker_up)
