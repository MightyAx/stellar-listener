import argparse

from stellar_listener.scanner import SkyScanner
from stellar_listener.transformer import OrientationTransformer

parser = argparse.ArgumentParser(description='Use SenseHat to determine Right Ascension and Declination')
parser.add_argument('latitude', type=float, help='Latitude of observer')
parser.add_argument('longitude', type=float, help='Longitude of observer')
parser.add_argument('elevation', type=float, help='Elevation of observer (in meters)')
args = vars(parser.parse_args())

latitude = args['latitude']
longitude = args['longitude']
elevation = args['elevation']

transformer = OrientationTransformer(latitude, longitude, elevation)
scanner = SkyScanner(transformer)
while True:
    scanner.scan()
