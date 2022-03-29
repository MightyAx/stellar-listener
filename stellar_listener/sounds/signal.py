import math
from abc import abstractmethod
from astropy.coordinates import SkyCoord, ICRS
from .base import BaseSound


class BaseSignal(BaseSound):
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