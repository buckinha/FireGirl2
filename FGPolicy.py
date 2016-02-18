import numpy as np
import random

class FGPolicy:
    """TODO"""

    def __init__(self):
        pass

    def __repr__(self):
        """TODO"""
        return "FGPolicy Object"


    def get_pol_decision(self, FGPathway_object, location, forecast):
        """Makes suppression decisions for the given ignition event.
        
        PARAMETERS
        ----------
        FGPathway_object, location, forecast

        FGPathway_object
            The FireGirl pathway  object on which this fire is occuring

        location
            A coordinate pair describing the ignition location

        forecast
            The weather forecast associated with this ignition; a 2-d list produced
            by a FGWeather.WeatherModel

        """

        pass




