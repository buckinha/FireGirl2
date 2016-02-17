import random

class SpreadModel:

    def __init__(self):
        pass

    def __repr__(self):
        """TODO"""
        return "FGFire.SpreadModel Object"


    def get_new_ignitions(self, FGPathway_object):
        """Returns a set of new FGFire.IgnEvent objects

        PARAMETERS
        ----------
        FGPathway_object: 
            The FGPathway object for which to draw ignitions

        
        RETURNS
        -------
        A list of FGFire.IgnEvent objects

        """

        pass


    def simulate_fire(self, FGPathway_object, FGFireEvent_object, suppression_choice):
        """
        Takes a FGPathway Object, and information about an ignition, and simulates a fire.

        PARAMETERS
        ----------
        FGPathway_object: 
            The FGPathway object on which this fire should be simulated

        FGFireEvent_object:
            A FGFireEvent object which contains the following:
            -- The (x,y) coordinates of the ignition location
            -- The duration of the fire (if unsuppressed), based on...
            -- The real weather stream
            -- The forecasted weather stream

        suppression_choice:
            A boolean, with True meaning, attempt suppression, and False meaning no 
            suppresion effort.


        RETURNS
        -------
        None
        """

        pass



class IgnEvent:
    """
    A FGFire.IgnEvent object contains the following information about a SINGLE FG Fire:
    -- The (x,y) coordinates of the ignition location
    -- The duration of the fire (if unsuppressed), based on...
    -- The real weather stream
    -- The forecasted weather stream
    """

    def __init__(self, date, random_seed=None):

        self.date = date

        self.loc = [0,0]
        self.duration = 1

        #weather information are as a list of lists:
        #each sub-list is a vector of one day's weather in the form
        #  [temperature, humidity, windspeed, wind_direction]
        self.real_weather = [[0,0,0,0]]
        self.forecast = [[0,0,0,0]]


    def __repr__(self):
        """TODO"""
        return "A FGFire.IgnEvent Object"


    def draw_weather(self, random_seed):
        """Draws new weather and forcasts, given a random seed"""

        pass


