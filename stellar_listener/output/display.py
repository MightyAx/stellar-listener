from sense_hat import SenseHat
from .images.base import BaseImage

class Display():
    def __init__(self, sense: SenseHat, rotation: int = 0, low_light: bool = True):
        self.sense = sense
        self.sense.rotation = rotation
        self.sense.low_light = low_light
        self.__off = 0
        self.__min = 1
        self.__max = 255
        self.__brightness = 127
        self.increment = 16
    
    @property
    def brightness(self):
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness: int):
        if brightness >= self.__min and brightness <= self.__max:
            print('Brightness set to: ' + str(brightness))
            self.__brightness = brightness
        else:
            raise ValueError('Brighness must be set between 1 and 255')
    
    def brightness_up(self):
        new_brightness = self.brightness + self.increment
        if new_brightness > self.__max:
            new_brightness = self.__max
        self.brightness = new_brightness

    def brightness_down(self):
        new_brightness = self.brightness - self.increment
        if new_brightness < self.__min:
            new_brightness = self.__min
        self.brightness = new_brightness
    
    def letter(self, letter: str, red: bool = False, green: bool = False, blue: bool = False):
        self.sense.show_letter(letter, text_colour=[self.brightness if red else self.__off, self.brightness if green else self.__off, self.brightness if blue else self.__off])

    def image(self, image: BaseImage):
        self.sense.set_pixels(image.output_at_brightness(self.brightness))

    def clear(self):
        self.sense.clear()