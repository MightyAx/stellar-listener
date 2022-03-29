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
        amplitude = self.map_seperation_to_amplitude(self.separation)
        super().apply_amplitude(amplitude)
    
    @abstractmethod
    def map_seperation_to_amplitude(self, seperation: int):
        pass