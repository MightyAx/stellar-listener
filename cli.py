import argparse
import math
import time

from sense_hat import SenseHat
from sonic_pi.tool import Server as SonicServer
from stellar_listener.transformer import OrientationTransformer
from stellar_listener.observer import SenseHatObserver
from stellar_listener.sound_maker import SoundMaker
from stellar_listener.images.colours import Red

parser = argparse.ArgumentParser(description='Use SenseHat to determine Right Ascension and Declination')
parser.add_argument('latitude', type=float, help='Latitude of observer')
parser.add_argument('longitude', type=float, help='Longitude of observer')
parser.add_argument('elevation', type=float, help='Elevation of observer (in meters)')
parser.add_argument('--rotation', type=int, choices=[0,90,180,270], default=90, help='Rotation of Pi Screen')
parser.add_argument('--bright', action='store_true', help="Turn off the sense hat's low-light mode.")
parser.add_argument('--fast_boot', action='store_true', help="Fast startup, should be off if being called on device boot.")
parser.add_argument('--host', default='127.0.0.1', help="IP or hostname of Sonic Pi server.")
parser.add_argument('--cmd-port', default=4557, help="Port number of Sonic Pi command server")
parser.add_argument('--osc-port', default=4560, help="Port number of Sonic Pi OSC cue server.")
parser.add_argument('--preamble', action='store_true', help="Send preamble to enable OSC server (needed on some Sonic Pi versions).")
parser.add_argument('--verbose', action='store_true', help="Print more information to help with debugging.")

args = vars(parser.parse_args())

sense = SenseHat()
sense.set_rotation(args['rotation'])
if (not args['bright']):
    sense.low_light = True

if (not args['fast_boot']):
    i = 9
    while i > 0:
        sense.show_letter(str(i), text_colour=Red)
        i = i - 1
        time.sleep(1)
sense.clear()

sonic = SonicServer(args['host'], args['cmd_port'], args['osc_port'], args['preamble'], args['verbose'])
transformer = OrientationTransformer(args['latitude'], args['longitude'], args['elevation'])
observer = SenseHatObserver(sense, transformer, args['rotation'])

with SoundMaker(sense, sonic, observer) as sounder:
    sounder.make_sound()
