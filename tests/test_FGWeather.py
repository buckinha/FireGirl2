import firegirl2.FGWeather
import random

def test_draw_weather_variables():
    weather_model = firegirl2.FGWeather.WeatherModel()
    #test for random seed consistency
    test_count = 1000
    random.seed(None)
    for i in range(test_count):
        seed = random.random()
        date = random.randint(1,365)
        val1 = weather_model.draw_weather_variables(date, seed)
        val2 = weather_model.draw_weather_variables(date, seed)
        assert val1 == val2

def test_draw_wind():
    weather_model = firegirl2.FGWeather.WeatherModel()
    #test for random seed consistency
    test_count = 1000
    random.seed(None)
    for i in range(test_count):
        seed = random.random()
        date = random.randint(1,365)
        val1 = weather_model.draw_wind(date, seed)
        val2 = weather_model.draw_wind(date, seed)
        assert val1 == val2


    #test range
    for i in range(test_count):
        val = weather_model.draw_wind(random.randint(1,365))
        assert val >= 0
        assert val < 200 #optional... theoretically, it could be

def test_draw_wind_direction():
    weather_model = firegirl2.FGWeather.WeatherModel()
    #test for random seed consistency
    test_count = 1000
    random.seed(None)
    for i in range(test_count):
        seed = random.random()
        date = random.randint(1,365)
        val1 = weather_model.draw_wind_direction(date, seed)
        val2 = weather_model.draw_wind_direction(date, seed)
        assert val1 == val2


    #test range
    for i in range(test_count):
        val = weather_model.draw_wind_direction(random.randint(1,365))
        assert val >= 0
        assert val < 365

def test_draw_temp():
    weather_model = firegirl2.FGWeather.WeatherModel()
    #test for random seed consistency
    test_count = 1000
    random.seed(None)
    for i in range(test_count):
        seed = random.random()
        date = random.randint(1,365)
        val1 = weather_model.draw_temp(date, seed)
        val2 = weather_model.draw_temp(date, seed)
        assert val1 == val2

    #test range
    for i in range(test_count):
        val = weather_model.draw_temp(random.randint(1,365))
        assert val >= -50
        assert val < 60

def test_draw_RH():
    weather_model = firegirl2.FGWeather.WeatherModel()
    #test for random seed consistency
    test_count = 1000
    random.seed(None)
    for i in range(test_count):
        seed = random.random()
        date = random.randint(1,365)
        val1 = weather_model.draw_RH(date, seed)
        val2 = weather_model.draw_RH(date, seed)
        assert val1 == val2

    #test range
    for i in range(test_count):
        val = weather_model.draw_RH(random.randint(1,365))
        assert val >= 0
        assert val < 100

def test_draw_rain():
    weather_model = firegirl2.FGWeather.WeatherModel()
    #test for random seed consistency
    test_count = 1000
    random.seed(None)
    for i in range(test_count):
        seed = random.random()
        date = random.randint(1,365)
        val1 = weather_model.draw_rain(date, seed)
        val2 = weather_model.draw_rain(date, seed)
        assert val1 == val2

    #test range
    for i in range(test_count):
        val = weather_model.draw_rain(random.randint(1,365))
        assert val >= 0
        assert val < 500

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

def test_get_new_fire_weather_stream_pair():
    #signature:
    #get_new_fire_weather_stream_pair(date, random_seed=None)
    #returns:
    #weather, forecast, each is a list. Each item in each list is a dictionary

    wm = firegirl2.FGWeather.WeatherModel()

    for i in range(1000):
        random.seed()
        streams = wm.get_new_fire_weather_stream_pair(random.randint(0,365))

        #forecast should always be length 3
        assert len(streams[1]) == 3

    #TODO, continue building this test.

def all_tests():
    test_get_month()
    test_draw_wind()
    test_draw_wind_direction()
    test_draw_temp()
    test_draw_RH()
    test_draw_rain()
    test_draw_weather_variables()


if __name__ == "__main__":
    all_tests()