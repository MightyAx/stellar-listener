from sense_hat import SenseHat
from astropy.time import Time
from .transformer import OrientationTransformer


class SenseHatObserver:
    def __init__(self, sense: SenseHat, transformer: OrientationTransformer):
        self.sense = sense
        self.transformer = transformer

    def make_observation(self):
        time = Time.now()
        orientation = self.sense.get_orientation()
        pitch, yaw = self.__adjust_observation(orientation)
        return self.transformer.get_sky_coord(pitch, yaw, time)
    
    def __adjust_observation(self, orientation):
        if (self.sense.rotation in [0, 180]):
            return self.__roll_as_pitch(orientation, self.sense.rotation == 180)
        return self.__pitch_as_pitch(orientation, self.sense.rotation == 270)
    
    def __pitch_as_pitch(self, orientation, flip=False):
        yaw = (orientation['yaw'] + self.sense.rotation - 90) % 360
        pitch = orientation['pitch']
        if pitch > 180:
            pitch = -1 * (360 - pitch)
        if (flip):
            pitch = -1 * pitch
        return pitch, yaw

    def __roll_as_pitch(self, orientation, flip=False):
        yaw = (orientation['yaw'] + self.sense.rotation - 90) % 360
        pitch = orientation['roll']
        if pitch > 90 and pitch < 270:
            yaw = (yaw + 180) % 360
            pitch = 180 - pitch
        if pitch > 270:
            pitch = -1 * (360 - pitch)
        if (flip):
            pitch = -1 * pitch
        return pitch, yaw
