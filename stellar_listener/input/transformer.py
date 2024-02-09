from astropy.coordinates import Latitude, Angle, Longitude, EarthLocation, AltAz, ICRS
from astropy.time import Time
from astropy.units import Quantity


class OrientationTransformer:
    def __init__(self, latitude: float, longitude: float, elevation: float):
        lat = Latitude(Angle(latitude, unit='deg'))
        lon = Longitude(Angle(longitude, unit='deg'))
        height = Quantity(elevation, unit='m')
        self.location = EarthLocation.from_geodetic(lon, lat, height)

    def get_sky_coord(self, pitch: float, yaw: float, time: Time = None):
        if not time:
            time = Time.now()
        alt = Angle(pitch, unit='deg')
        az = Angle(yaw, unit='deg')
        local_observation = AltAz(az=az, alt=alt, obstime=time, location=self.location)
        return local_observation.transform_to(ICRS())

