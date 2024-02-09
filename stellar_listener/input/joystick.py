from sense_hat import SenseHat, InputEvent, ACTION_RELEASED

up = 'up'
down = 'down'
left = 'left'
right = 'right'
middle = 'middle'

class Joystick():
    def __init__(self, sense: SenseHat):
        self.sense = sense
        self.callback_up = self.up
        self.callback_down = self.down
        self.callback_left = self.left
        self.callback_right = self.right
        self.callback_middle = self.middle
    
    def handle_events(self):
        """
        Handles all joystick events that occured since the last call
        returns true if there were any events to handle
        """

        joystick_used = False
        for event in self.sense.stick.get_events():
            if event.action != ACTION_RELEASED:
                joystick_used = True
                self.hande_direction(self.get_rotated_direction(self.sense.rotation, event.direction))
        return joystick_used
    
    def hande_direction(self, direction: str):
        if direction == up:
            self.callback_up()
        elif direction == down:
            self.callback_down()
        elif direction == left:
            self.callback_left()
        elif direction == right:
            self.callback_right()
        elif direction == middle:
            self.callback_middle()
    
    @staticmethod
    def up():
        print('Up')

    @staticmethod
    def down():
        print('Down')

    @staticmethod
    def left():
        print('Left')

    @staticmethod
    def right():
        print('Right')

    @staticmethod
    def middle():
        print('Middle')
    
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
