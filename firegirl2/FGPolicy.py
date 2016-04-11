import numpy as np
import random

class FGPolicy:
    """TODO"""

    def __init__(self):
        pass

    def __repr__(self):
        """TODO"""
        return "FGPolicy Object"


    def get_pol_decisions(self, FGPathway_object, locations, forecasts):
        """Makes suppression decisions for the given ignition event or events.
        
        PARAMETERS
        ----------
        FGPathway_object, locations, forecasts

        FGPathway_object
            The FireGirl pathway  object on which this fire is occuring

        locations
            A list of coordinate pairs describing each ignition location

        forecasts
            The weather forecasts associated with each ignition; each one is a
             dictionary produced by a FGWeather.WeatherModel

        """

        #check to see if only a single ignition has been passed in, rather than a list of them
        if hasattr(locations[0], '__iter__'):
            #this is a list of locations, so leave it as it stands
            pass
        else:
            #the sub item is NOT iterable, so it is probably a single coordinate value, so:
            locations = [locations]
            forecasts = [forecasts]

        decisions = [ self.get_decision(FGPathway_object, loc, fc) for loc, fc in zip(locations, forecasts) ]

        return decisions


    def get_decision(FGPathway_object, location, forecast):
        """Makes a single suppression decision for a given ignition event.


        PARAMETERS
        ----------
        FGPathway_object, locations, forecasts

        FGPathway_object
            The FireGirl pathway  object on which this fire is occuring

        location
            The coordinate pair describing the ignition location

        forecast
            The weather forecast associated with the ignition; it is a
             dictionary produced by a FGWeather.WeatherModel

        """
        #TODO
        return False