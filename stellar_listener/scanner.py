import math

from astropy.coordinates import SkyCoord, Angle
from astropy.time import Time
from sense_hat import SenseHat

from stellar_listener.transformer import OrientationTransformer


class SkyScanner:
    def __init__(self, transformer: OrientationTransformer):
        self.sense = SenseHat()
        self.sense.set_rotation(90)
        self.transformer = transformer
        self.polaris = SkyCoord.from_name('polaris')

    def scan(self):
        time = Time.now()
        o = self.sense.get_orientation()
        pitch = o['pitch']
        yaw = o['yaw']
        observation = self.transformer.get_sky_coord(pitch, yaw, time)
        separation = observation.separation(self.polaris)
        print(separation)
        if separation.is_within_bounds(upper=Angle(9.9, unit='deg')):
            self.sense.show_letter(str(math.floor(separation.dms.d)), text_colour=[0, 0, 255])
        else:
            self.sense.clear()
