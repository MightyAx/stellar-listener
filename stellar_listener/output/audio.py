from typing import List

from sonic_pi.tool import Server as SonicServer
from .sounds.base import BaseSound


class Audio():
    def __init__(self, sonic: SonicServer):
        self.sonic = sonic
        self.__min = 0
        self.__max = 100
        self.increment = 5
        self.__volume = 50
        self.sounds = []

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, volume: int):
        if volume >= self.__min and volume <= self.__max:
            print('Volume set to: ' + str(volume))
            self.__volume = volume
            self.apply_volume_to_sounds()
        else:
            raise ValueError('Volume must be set between 0 and 100')
    
    @property
    def volume_fraction(self):
        return self.volume / self.__max

    def volume_up(self):
        new_volume = self.volume + self.increment
        if new_volume > self.__max:
            new_volume = self.__max
        self.volume = new_volume

    def volume_down(self):
        new_volume = self.volume - self.increment
        if new_volume < self.__min:
            new_volume = self.__min
        self.volume = new_volume
    
    def apply_volume_to_sounds(self):
        for sound in self.sounds:
            self.__apply_volume(sound, self.volume_fraction)

    def init_sounds(self):
        self.__send_sonic([s.start for s in self.sounds])

    def send_sounds(self):
        self.__send_sonic([s.sound for s in self.sounds])
   
    def __send_sonic(self, sounds: List[str]):
        code = '\r\n'.join(sounds)
        self.sonic.run_code(code)
 
    @staticmethod
    def __apply_volume(sound: BaseSound, volume: float):
        sound.volume = volume

