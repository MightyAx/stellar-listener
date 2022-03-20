import argparse

from sonic_pi.tool import Installation, Server
from stellar_listener.scanner import SkyScanner
from stellar_listener.transformer import OrientationTransformer

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

inst = Installation.get_installation((), args['verbose'])
if not inst:
    raise RuntimeError('No Sonic Pi found')

sonic = Server(args['host'], args['cmd_port'], args['osc_port'], args['preamble'], args['verbose'])
if sonic.check_if_running() == 2:
    sonic.shutdown_sonic_pi()

if sonic.check_if_running() == 1:
    def start():
        sonic.send_cmd('/cue-port-start')
        sonic.send_cmd('/cue-port-internal')
        sonic.send_cmd('/run-code', Server.preamble.format(sonic.get_cmd_port()))
    inst.run(True, start())

if sonic.check_if_running() != 0:
    raise RuntimeError('Could not start Sonic Pi')

start_file = ''
change_file = ''
with open('sounds/start.rb') as file:
    start_file = file.read()
if not start_file:
    raise RuntimeError('Could not read starting sounds file')
with open('sounds/change.rb') as file:
    change_file = file.read()
if not change_file:
    raise RuntimeError('Could not read dynamic sounds file')

sonic.run_code(start_file)
transformer = OrientationTransformer(args['latitude'], args['longitude'], args['elevation'])
scanner = SkyScanner(transformer)
while True:
    seperation = scanner.scan()
    amp = seperation.dms.d / 180
    sonic.run_code(change_file.format(vega=1-amp,white=amp))