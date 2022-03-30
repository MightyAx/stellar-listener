from sense_hat import SenseHat
from astropy.time import Time
from .transformer import OrientationTransformer


class SenseHatObserver:
    def __init__(self, sense: SenseHat, transformer: OrientationTransformer):
        self.sense = sense
        self.transformer = transformer

    def make_observation(self):
        time = Time.now()
        o = self.sense.get_orientation()
        pitch = o['pitch']
        yaw = o['yaw']
        return self.transformer.get_sky_coord(pitch, yaw, time)
