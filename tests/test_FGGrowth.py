from firegirl2 import FGGrowth
import math, random

def test_get_volume():
    growth_model = FGGrowth.GrowthModel()

    test_count = 1000

    for i in range(test_count):
        #let age get quite high, but lower cap at zero
        age = random.uniform(0,1000)
        #constrain site index to values between 0 and 100
        site_index = random.uniform(0,100)

        v = growth_model.get_volume(age, site_index)

        assert v >= 0

def test_get_ladder_fuel():
    growth_model = FGGrowth.GrowthModel()

    test_count = 1000

    for i in range(test_count):
        #let age get quite high, but lower cap at zero
        age = random.uniform(0,1000)
        #constrain site index to values between 0 and 100
        site_index = random.uniform(0,100)

        l = growth_model.get_ladder_fuel(age)
        
        assert l >= 0
        assert l <= 100

def test_get_surface_fuel():
    growth_model = FGGrowth.GrowthModel()

    test_count = 1000

    for i in range(test_count):
        #let age get quite high, but lower cap at zero
        age = random.uniform(0,1000)

        s = growth_model.get_surface_fuel(age)

        assert s >= 0
        assert s <= 100

def all_tests():
    test_get_volume()
    test_get_surface_fuel()
    test_get_ladder_fuel()


if __name__ == "__main__":
    all_tests()