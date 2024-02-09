import argparse
import math
import time

from sense_hat import SenseHat
from sonic_pi.tool import Server as SonicServer
from stellar_listener.output.display import Display
from stellar_listener.output.audio import Audio
from stellar_listener.input.gyroscope import Gyroscope
from stellar_listener.input.transformer import OrientationTransformer
from stellar_listener.input.joystick import Joystick
from stellar_listener.listener import Listener

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

display = Display(sense, args['rotation'], not args['bright'])
gyroscope = Gyroscope(sense, OrientationTransformer(args['latitude'], args['longitude'], args['elevation']))
joystick = Joystick(sense)

if (not args['fast_boot']):
    i = 9
    while i > 0:
        display.letter(str(i), red=True)
        i = i - 1
        time.sleep(1)
display.clear()

audio = Audio(SonicServer(args['host'], args['cmd_port'], args['osc_port'], args['preamble'], args['verbose']))

with Listener(display, audio, gyroscope, joystick) as listener:
    listener.listen()
