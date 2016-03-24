#firegir2/tests/test_main.py

import test_sigmoid
import test_FGGrowth
import test_FGWeather

if __name__ == "__main__":
    test_sigmoid.all_tests()
    test_FGGrowth.all_tests()
    test_FGWeather.all_tests()
    print("All Tests Passed")