import math
import unittest

from astropy.coordinates import Angle, AltAz, SkyCoord
from astropy.time import Time

from stellar_listener.transformer import OrientationTransformer


class TestOrientationTransformer(unittest.TestCase):
    def setUp(self) -> None:
        self.polaris = SkyCoord.from_name('polaris')
        self.now = Time.now()
        self.transformer = OrientationTransformer(0, 0, 0)
        local_frame = AltAz(obstime=self.now, location=self.transformer.location)
        self.local_polaris = self.polaris.transform_to(local_frame)

    def test_polaris(self):
        pitch = math.floor(self.local_polaris.alt.dms.d)
        yaw = math.floor(self.local_polaris.az.dms.d)
        sky_observation = self.transformer.get_sky_coord(pitch, yaw, self.now)
        angle = sky_observation.separation(self.polaris)
        self.assertTrue(angle.is_within_bounds(upper=Angle(2, unit='deg')))

    def test_bounds(self):
        pitch = math.floor(self.local_polaris.alt.dms.d)
        yaw = math.floor(self.local_polaris.az.dms.d)
        sky_observation1 = self.transformer.get_sky_coord(pitch, yaw, self.now)
        sky_observation2 = self.transformer.get_sky_coord(pitch + 1, yaw + 1, self.now)
        angle = sky_observation1.separation(sky_observation2)
        self.assertTrue(angle.is_within_bounds(upper=Angle(2, unit='deg')))
