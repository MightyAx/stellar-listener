import argparse
import math

from sense_hat import SenseHat
from sonic_pi.tool import Server as SonicServer
from stellar_listener.transformer import OrientationTransformer
from stellar_listener.observer import SenseHatObserver
from stellar_listener.sound_maker import SoundMaker

parser = argparse.ArgumentParser(description='Use SenseHat to determine Right Ascension and Declination')
parser.add_argument('latitude', type=float, help='Latitude of observer')
parser.add_argument('longitude', type=float, help='Longitude of observer')
parser.add_argument('elevation', type=float, help='Elevation of observer (in meters)')
parser.add_argument('--host', default='127.0.0.1', help="IP or hostname of Sonic Pi server.")
parser.add_argument('--cmd-port', default=4557, help="Port number of Sonic Pi command server")
parser.add_argument('--osc-port', default=4560, help="Port number of Sonic Pi OSC cue server.")
parser.add_argument('--preamble', action='store_true', help="Send preamble to enable OSC server (needed on some Sonic Pi versions).")
parser.add_argument('--verbose', action='store_true', help="Print more information to help with debugging.")
args = vars(parser.parse_args())

sense = SenseHat()
sense.set_rotation(90)

sonic = SonicServer(args['host'], args['cmd_port'], args['osc_port'], args['preamble'], args['verbose'])
transformer = OrientationTransformer(args['latitude'], args['longitude'], args['elevation'])
observer = SenseHatObserver(sense, transformer)

with SoundMaker(sense, sonic, observer) as sounder:
    sounder.make_sound()
