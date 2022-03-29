import os
import math
from abc import ABCMeta, abstractmethod
from pathlib import Path

from astropy.coordinates import SkyCoord, ICRS

class BaseSound(metaclass = ABCMeta):
    def __init__(self, name):
        self.name = name
        self.start = self.__read_file(f'start/{name}.rb')
        self.__update = self.__read_file(f'update/{name}.rb')
        self.amplitude = None
        self.sound = None
        
    def apply_amplitude(self, amplitude):
        self.amplitude = amplitude
        self.sound = self.__update.format(amp=amplitude)

    @staticmethod
    def __read_file(file_name):
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        content = None
        with open(Path(file_path)) as file:
            content = file.read()
        if not content:
            raise RuntimeError(f'Could not read sounds file: {file_name}')
        return content

class BaseSoundCoord(BaseSound):
    def __init__(self, name, colour, astropy_name = None):
        super().__init__(name)
        self.coord = SkyCoord.from_name(astropy_name if astropy_name else name)
        self.colour = colour
        self.seperation = None
    
    def apply_observation(self, observation: ICRS):
        self.separation = math.floor(observation.separation(self.coord).dms.d)
        amplitute = self.map_seperation_to_amplitute(self.separation)
        super().apply_amplitude(amplitute)
    
    @abstractmethod
    def map_seperation_to_amplitute(self, seperation: int):
        pass
