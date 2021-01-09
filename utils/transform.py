import argparse
from sense_hat import SenseHat
from astropy.units import Quantity
from astropy.coordinates import EarthLocation, Angle, Latitude, Longitude, AltAz, ICRS
from astropy.time import Time


def get_altitude(pitch: float) -> float:
    if pitch > 180:
        return -1 * (360 - pitch)
    return pitch


def get_azimuth(yaw: float) -> float:
    return (yaw + 180) % 360  # Southward origin increasing westward


parser = argparse.ArgumentParser(description='Use SenseHat to determine Right Ascension and Declination')
parser.add_argument('latitude', type=float, help='Latitude of observer')
parser.add_argument('longitude', type=float, help='Longitude of observer')
parser.add_argument('elevation', type=float, help='Elevation of observer (in meters)')
args = vars(parser.parse_args())

latitude = Latitude(Angle(args['latitude'], unit='deg'))
longitude = Longitude(Angle(args['longitude'], unit='deg'))
height = Quantity(args['elevation'], unit='m')
location = EarthLocation.from_geodetic(lat=latitude, lon=longitude, height=height)
sense = SenseHat()
while True:
    sense.clear()
    o = sense.get_orientation()
    now = Time.now()
    # CouldDo: Retrieve GPS Coordinates here

    alt = Angle(get_altitude(o["pitch"]), unit='deg')
    az = Angle(get_azimuth(o["yaw"]), unit='deg')
    local_observation = AltAz(location=location, obstime=now, az=az, alt=alt)
    icrs_observation = local_observation.transform_to(ICRS())

    declination = icrs_observation.dec
    right_ascension = icrs_observation.ra

    print("altitude", alt)
    print("azimuth", az)
    print("declination", declination)
    print("right ascension", right_ascension)
