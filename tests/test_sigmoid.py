import math, random
import numpy as np
from utils import sigmoid

def test_min_max():
    #function signature:
    #sigmoid(x, center=0.0, min_val=0.0, max_val=1.0)
    test_count = 1000
    sample_count = 1000

    for i in range(test_count):
        a = random.uniform(-1000,1000)
        b = random.uniform(-1000,1000)
        while a == b:
            b = random.uniform(-1000,1000)

        max_val = max(a, b)
        min_val = min(a, b)

        center = random.uniform(-1000,1000)

        samples = [ sigmoid.sigmoid(random.uniform(-10000,10000), center, min_val, max_val) for j in range(sample_count)]

        sample_range = max_val - min_val

        assert (min(samples) - min_val) < (0.05 * sample_range)
        assert (max_val - max(samples)) < (0.05 * sample_range)
        

def test_center():
    #function signature:
    #sigmoid(x, center=0.0, min_val=0.0, max_val=1.0)
    test_count = 1000
    sample_count = 1

    for i in range(test_count):
        a = random.uniform(-1000,1000)
        b = random.uniform(-1000,1000)
        while a == b:
            b = random.uniform(-1000,1000)

        max_val = max(a, b)
        min_val = min(a, b)

        center = random.uniform(-1000,1000)
        mid_val = (max_val - min_val)/2.0 + min_val

        for j in range(sample_count):
            center_val = sigmoid.sigmoid(x=center, center=center, min_val=min_val, max_val=max_val)
            assert np.allclose( center_val , mid_val)



def all_tests():
    test_min_max()
    test_center()


if __name__ == "__main__":
    all_tests()