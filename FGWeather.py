#FGWeather.py
#FireGirl Weather Model

class WeatherModel:
    """Model for producing weather streams and weather forecasts for FireGirl"""

    def __init__(self):
        pass

    def __repr__(self):
        """TODO"""
        return "A WeatherModel object"


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