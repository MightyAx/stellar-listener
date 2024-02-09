from abc import ABCMeta
from typing import List


O = False
X = True

class BaseImage(metaclass = ABCMeta):
    def __init__(self, pixel_list: List[bool], red: bool = False, green: bool = False, blue: bool = False):
        self.pixels = pixel_list
        self.rgb = [red, green, blue]
    
    def output_at_brightness(self, brighness: int):
        bright_colour = self.__get_colour(brighness)
        matrix = []
        for pixel in self.pixels:
            matrix.append(bright_colour if pixel else [0, 0, 0])
        return matrix
    
    def __get_colour(self, brighness: int):
        bright_colour = []
        for colour in self.rgb:
                bright_colour.append(brighness if colour else 0)
        return bright_colour
