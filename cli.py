import argparse
import math
from stellar_listener.server import StellarServer

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

stellar = StellarServer()
stellar.start_sonic(args['host'], args['cmd_port'], args['osc_port'], args['preamble'], args['verbose'])
stellar.add_scanner(args['latitude'], args['longitude'], args['elevation'])
stellar.add_sounds('sounds/start.rb', 'sounds/change.rb')

# ToDo: Monitor for key press
# ToDo: push this while into StellarServer
# ToDo: Wrap in a closing with stop
stellar.start_sound()
while True:
    seperation = math.floor(stellar.scanner.scan().dms.d)
    if (seperation != stellar.last_seperation):
        stellar.update_sound(seperation)
