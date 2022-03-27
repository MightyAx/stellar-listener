from pathlib import Path
from ratelimit import limits

from sonic_pi.tool import Installation, Server
from .scanner import SkyScanner
from .transformer import OrientationTransformer

class StellarServer:
    def __init__(self):
        self.sonic = None
        self.scanner = None 
        self.initial_sound = None
        self.change_sound = None
        self.last_seperation = None

    def start_sonic(self, host: str, cmd_port: int, osc_port: int, preamble: bool, verbose: bool):
        install = Installation.get_installation((), verbose)
        if not install:
            raise RuntimeError('No Sonic Pi found')
        self.sonic = Server(host, cmd_port, osc_port, preamble, verbose)

        if self.sonic.check_if_running() == 2:
            self.sonic.shutdown_sonic_pi()

        if self.sonic.check_if_running() == 1:
            install.run(True, self.__send_start())

        if self.sonic.check_if_running() != 0:
            raise RuntimeError('Could not start Sonic Pi')
    
    def add_scanner(self, latitude: float, longitude: float, elevation: float):
        transformer = OrientationTransformer(latitude, longitude, elevation)
        self.scanner = SkyScanner(transformer)
        
    def add_sounds(self, init_sound_path: str, dynamic_sound_path: str):
        with open(Path(init_sound_path)) as file:
            self.initial_sound = file.read()
        if not self.initial_sound:
            raise RuntimeError('Could not read starting sounds file')
        with open(Path(dynamic_sound_path)) as file:
            self.change_sound = file.read()
        if not self.change_sound:
            raise RuntimeError('Could not read dynamic sounds file')

    def start_sound(self):
        self.sonic.run_code(self.initial_sound)
    
    @limits(calls=1, period=1, raise_on_limit=False)
    def update_sound(self, seperation):
        self.last_seperation = seperation
        amp = seperation / 180
        updated_sound = self.change_sound.format(vega=1-amp,white=amp)
        self.sonic.run_code(updated_sound)
    
    def __send_start(self):
        self.sonic.send_cmd('/cue-port-start')
        self.sonic.send_cmd('/cue-port-internal')
        self.sonic.send_cmd('/run-code', Server.preamble.format(self.sonic.get_cmd_port()))
