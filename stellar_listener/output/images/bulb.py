from .base import BaseImage, O, X

class BulbOff(BaseImage):
    def __init__(self):
        super().__init__([
            O, O, O, X, X, O, O, O,
            O, O, X, O, O, X, O, O,
            O, X, O, O, O, O, X, O,
            O, X, O, O, O, O, X, O,
            O, O, X, O, O, X, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O
            ], red=True, green=True, blue=True)

class BulbOn(BaseImage):
    def __init__(self):
        super().__init__([
            O, O, O, X, X, O, O, O,
            O, O, X, X, X, X, O, O,
            O, X, X, X, X, X, X, O,
            O, X, X, X, X, X, X, O,
            O, O, X, X, X, X, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O
            ], red=True, green=True, blue=True)
