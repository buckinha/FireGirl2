import math

def sigmoid(x, center=0.0, min_val=0.0, max_val=1.0):
    _x = x - center
    if _x > 500: _x = 500
    if _x < -500: _x = -500
    return ((max_val-min_val) / (1 + math.exp(-1.0 * _x ))) + min_val