from .colours import Black, White

O = Black
X = White

BULB_OFF = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, X, O, O, O, O, X, O,
O, X, O, O, O, O, X, O,
O, O, X, O, O, X, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O
]

BULB_ON = [
O, O, O, X, X, O, O, O,
O, O, X, X, X, X, O, O,
O, X, X, X, X, X, X, O,
O, X, X, X, X, X, X, O,
O, O, X, X, X, X, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O
]
