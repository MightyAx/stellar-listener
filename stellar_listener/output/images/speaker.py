from .base import BaseImage, O, X

class SpeakerDown(BaseImage):
    def __init__(self):
        super().__init__([
            O, O, O, X, O, O, O, O,
            O, O, X, X, O, O, O, O,
            O, X, X, X, O, O, O, O,
            X, X, X, X, O, O, O, O,
            X, X, X, X, O, O, O, O,
            O, X, X, X, O, O, O, O,
            O, O, X, X, O, O, O, O,
            O, O, O, X, O, O, O, O
            ], red=True, green=True, blue=True)

speaker_down = SpeakerDown()

class SpeakerUp(BaseImage):
    def __init__(self):
        super().__init__([
            O, O, O, X, O, O, O, O,
            O, O, X, X, O, X, O, O,
            O, X, X, X, O, O, X, O,
            X, X, X, X, O, O, O, X,
            X, X, X, X, O, O, O, X,
            O, X, X, X, O, O, X, O,
            O, O, X, X, O, X, O, O,
            O, O, O, X, O, O, O, O
            ], red=True, green=True, blue=True)

speaker_up = SpeakerUp()
