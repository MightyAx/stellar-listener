import argparse
from datetime import datetime, timezone
from math import sin, cos, tan, asin, atan
from sense_hat import SenseHat


def get_altitude(pitch: float) -> float:
    if pitch > 180:
        return -1 * (360 - pitch)
    return pitch


def get_azimuth(yaw: float) -> float:
    return (yaw + 180) % 360  # Southward origin increasing westward


def get_local_hour_angle(azimuth: float, latitude: float, altitude: float) -> float:
    return atan(sin(azimuth) / (cos(azimuth) * sin(latitude) + tan(altitude) * cos(latitude)))


def get_declination(latitude: float, altitude: float, azimuth: float) -> float:
    return asin(sin(latitude) * sin(altitude) - cos(latitude) * cos(altitude) * cos(azimuth))


def get_local_sidereal_time(date_time: datetime, longitude: float) -> float:
    year_constant = 6.5772495  # Approx 2020 from 2011 constant 6.6208844
    day_of_year = date_time.timetuple().tm_yday
    hour_of_day = date_time.hour + (date_time.minute / 60) + (date_time.second / (60 * 60))
    greenwich_sidereal_time = (year_constant + day_of_year * 0.0657098244 + hour_of_day * 1.00273791) % 24
    return greenwich_sidereal_time + longitude


def get_right_ascension(local_sidereal_time: float, local_hour_angle:float) -> float:
    return local_sidereal_time - local_hour_angle


parser = argparse.ArgumentParser(description='Use SenseHat to determine Right Ascension and Declination')
parser.add_argument('latitude', type=float, help='Latitude of observer')
parser.add_argument('longitude', type=float, help='Longitude of observer')
args = vars(parser.parse_args())

lat = args['latitude']
long = args['longitude']
sense = SenseHat()
while True:
    sense.clear()
    o = sense.get_orientation()
    now = datetime.now(timezone.utc)
    # CouldDo: Retrieve GPS Coordinates here

    alt = get_altitude(o["pitch"])
    azi = get_azimuth(o["yaw"])

    declination = get_declination(lat, alt, azi)
    right_ascension = get_right_ascension(
        get_local_sidereal_time(now, long),
        get_local_hour_angle(azi, lat, alt)
    )
    print("altitude", alt)
    print("azimuth", azi)
    print("declination", declination)
    print("right ascension", right_ascension)
