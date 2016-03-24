import firegirl2.FGWeather
import random

def test_get_month():
    WM = firegirl2.FGWeather.WeatherModel()

    test_count = 5000

    #random testing
    for i in range(test_count):
        month = WM.get_month(random.uniform(-100000,100000))
        assert ( month >= 0) and (month <=12)


    #test all normal values
    actual_days_in_month = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    counted_days_in_month = [0]*12

    for i in range(1,366):
        month = WM.get_month(i)
        counted_days_in_month[month-1] += 1

    assert counted_days_in_month == actual_days_in_month


def all_tests():
    test_get_month()


if __name__ == "__main__":
    all_tests()