from sense_hat import SenseHat, InputEvent, ACTION_RELEASED
from .images.bulb import BULB_ON, BULB_OFF

up = 'up'
down = 'down'
left = 'left'
right = 'right'
middle = 'middle'

class JoystickHandler():
    def __init__(self, sense: SenseHat, screen_rotation: int):
        self.sense = sense
        self.rotation = screen_rotation
    
    def handle_joystick_events(self):
        joystick_used = False
        for event in self.sense.stick.get_events():
            if event.action != ACTION_RELEASED:
                joystick_used = True
                self.hande_direction(self.get_rotated_direction(self.rotation, event.direction))
        return joystick_used
    
    def hande_direction(self, direction: str):
        if direction == up:
            print('Brightness Up')
            self.sense.set_pixels(BULB_ON)
        elif direction == down:
            print('Brightness Down')
            self.sense.set_pixels(BULB_OFF)
        elif direction == left:
            print('Volume Down')
        elif direction == right:
            print('Volume Up')
        elif direction == middle:
            print('Toggle Padlock')
    
    @staticmethod
    def get_rotated_direction(rotation: int, direction: str):
        if direction == middle:
            return middle
        if ((rotation == 0 and direction == up)
            or (rotation == 90 and direction == right) 
            or (rotation == 180 and direction == down)
            or (rotation == 270 and direction == left)):
            return up
        if ((rotation == 0 and direction == right)
            or (rotation == 90 and direction == down)
            or (rotation == 180 and direction == left)
            or (rotation == 270 and direction == up)):
            return right
        if ((rotation == 0 and direction == down)
            or (rotation == 90 and direction == left)
            or (rotation == 180 and direction == up)
            or (rotation == 270 and direction == right)):
            return down
        if ((rotation == 0 and direction == left)
            or (rotation == 90 and direction == up)
            or (rotation == 180 and direction == right)
            or (rotation == 270 and direction == down)):
            return left
