import os
from abc import ABCMeta
from pathlib import Path


class BaseSound(metaclass = ABCMeta):
    def __init__(self, name: str):
        self.name = name
        self.start = self.__read_file(f'start/{name}.rb')
        self.__update = self.__read_file(f'update/{name}.rb')
        self.amplitude = None
        self.sound = None
        
    def apply_amplitude(self, amplitude):
        self.amplitude = amplitude
        self.sound = self.__update.format(amp=amplitude)

    @staticmethod
    def __read_file(file_name: str):
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        content = None
        with open(Path(file_path)) as file:
            content = file.read()
        if not content:
            raise RuntimeError(f'Could not read sounds file: {file_name}')
        return content
