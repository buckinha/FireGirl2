#firegirl2/FGWeather.py
#FireGirl Weather Model

import utils.FWIFunctions as FWI

class WeatherModel:
    """Model for producing weather streams and weather forecasts for FireGirl"""

    def __init__(self):
        pass

    def __repr__(self):
        """TODO"""
        return "A FireGirl2 WeatherModel object"


    def get_new_fire_weather(self, date, random_seed=None):
        """Creates a new weather stream and forcast

        PARAMETERS
        ----------
        date
            the integer date of the year

        random_seed
            Any hashable value for seeding the weather/forecast generation process.
            Ensures replicability.

        RETURNS
        -------
        weather, forecast
        
        weather 
            A 2-d list of weather variables with the primary index being day.
        forcast
            The associated weather forcast, of identical shape as "weather"

        """

        weather = []
        forecast = []

        return weather, forecast

    def get_new_fires(self, random_seed=None):
        """Generates a new series of fires for a simulation year and returns any/all of them

        PARAMETERS
        ----------
        random_seed
            Any hashable value for seeding the weather/forecast generation process.
            Ensures replicability.


        RETURNS
        -------
        weather_streams, forecasts

        weather_streams
            A list of weather streams. Each weather stream is a 2-d list, indexed by day,
            of a particular fire/weather event.

        forecasts
            A list of weather forecasts. Each forecast is a a 2-d list, indexed by day, of
            weather forecast information for a particular fire/weather event.

        """

        weather_streams = []
        forecasts = []

        return weather_streams, forecasts


    def draw_weather_variables(self, date, random_seed=None):
        """Draws random weather variables and derived values, given the integer date"""
        pass

    def get_month(self, day):
        """Return the numeral month, given the day-of-the-year"""
        if day <= 31:
            #january
            return 1
        elif day <= (31+28):
            #february
            return 2
        elif day <= (31+28+31):
            #march
            return 3
        elif day <= (31+28+31+30):
            #april
            return 4
        elif day <= (31+28+31+30+31):
            #may
            return 5
        elif day <= (31+28+31+30+31+30):
            #june
            return 6
        elif day <= (31+28+31+30+31+30+31):
            #july
            return 7
        elif day <= (31+28+31+30+31+30+31+31):
            #august
            return 8
        elif day <= (31+28+31+30+31+30+31+31+30):
            #september
            return 9
        elif day <= (31+28+31+30+31+30+31+31+30+31):
            #october
            return 10
        elif day <= (31+28+31+30+31+30+31+31+30+31+30):
            #november
            return 11
        else:
            #december
            return 12