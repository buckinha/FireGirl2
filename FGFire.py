import random, Queue
import numpy as np

class SpreadModel:

    def __init__(self):
        pass

    def __repr__(self):
        """TODO"""
        return "FGFire.SpreadModel Object"


    def simulate_fire(self, FGPathway_object, location, weather, supr_decision):
        """
        Takes a FGPathway Object, and information about an ignition, and simulates a fire.

        Modifies FGPathway in place.

        PARAMETERS
        ----------
        FGPathway_object: 
            The FGPathway object on which this fire should be simulated

        location
            the coordinate pair representing the ignition location on the landscape

        weather
            The weather stream. A 2-d list generated by FGWeather.WeatherModel containing
            information about each day's weather (indexed by day)

        supr_decision:
            A boolean, with True meaning, attempt suppression, and False meaning no 
            suppresion effort.


        RETURNS
        -------
        FireRecord object
        """


        ######################################
        #  Initialize the fire sequence
        ######################################
        current_day = 0
        current_time = 0.0
        cells_burned = 0
        cells_crowned = 0
        spreading = False
        loc = location[:]
        sppr_dec = supr_decision

        # 1) is this fire going to spread at all?
        init_ignitions = get_neighbor_ignitions(FGPathway_object, loc, weather[current_day], sppr_dec)
        if len(init_ignitions) > 0:
            #if the spreadrate was zero, then there will be nothing in this list
            #since there IS at least one item, there is some spread
            spreading = True

        if not spreading:
            fr = FireRecord()
            fr.ignition_location=location[:]
            fr.weather = [weather[0][:]] #only including the first day of weather
            fr.suppressed = sppr_dec
            return fr

        #initialize the priority queue
        pq = Queue.PriorityQueue()

        #initialize the burn maps
        burn_map = np.zeros(FGPathway_object.size, dtype='int')
        crown_burn_map = np.zeros(FGPathway_object.size, dtype='int')

        #add the initial ignition location to the queue
        pq.put((current_time, loc[0], loc[1]))

        #the weather stream is arranged by day, so if the weather model gave us 4 days
        # to spread a fire (before a fire-ending weather event), it will have length 4.
        #We want to spread a fire for four whole days, starting at time = 0, and ending
        # at time = 3.9999, for a total of 4 "time units" which is represents four days.
        max_time = len(weather)

        #start the loop, and continue while there's anything queued, or until time expires
        while (current_time < max_time) and not (pq.empty()):
            #get the next queue item
            current_cell = pq.get()
            loc = (current_cell[1], current_cell[2])

            #increment current time to this cell's ignition time
            current_time = current_cell[0]
            #adjust day, if needed
            if current_time - current_day >= 1.0:
                current_day += 1

            #check to see if this cell has already been burned
            if burn_map[loc[0], loc[1]:
                #it's already burned in a previous step, so lets move on
                continue
            
            #we haven't 'continued', so this cell hasn't burned yet.
            # a) update the burn map
            burn_map[loc[0], loc[1]] = 1
            cells_burned += 1

            # b) check for crown fire, and if necessary, update the crown burn map
            if get_crown_burn(FGPathway_object, loc, weather[current_day], sppr_dec):
                crown_burn_map[loc[0], loc[1]] = 1
                cells_crowned += 1
            
            # c) get the neighbor ignitions
            n_igns = get_neighbor_ignitions(FGPathway_object, loc, weather[current_day], sppr_dec)

            # d) add ignitions to the priority queue
            for i in n_igns:
                pq.put(i)


        #all done with the queue, so either we ran out of new cells, or the time expired
        fr = FireRecord()
        fr.acres_burned = cells_burned
        fr.acres_crown_burned = cells_crowned
        fr.weather = weather[:]
        fr.suppressed = sppr_dec
        fr.ignition_location = location[:]

        fr.suppression_cost = calc_suppression_cost(fr)

        return fr




def calc_suppression_cost(fire_record):
    return 0.0

def get_neighbor_ignitions(FGPathway_object, location, weather_today, supr_dec):
    """

    RETURNS
    (ignition_time, location_x, location_y)
    """
    return []

def get_crown_burn(FGPathway_object, loc, weather[current_day], sppr_dec):
    """
    RETURNS
    -------
    boolean, True indicates that this cell has a burned crown, False not.
    """

    return False


class FireRecord:
    """Records information about a single fire, within a single simulation year."""

    def __init__(self):
        self.ignition_location = (0,0)
        self.weather = [] #the weather list, originally produced by FGWeather.WeatherModel
        self.suppressed = False #was suppression applied to this fire?
        self.suppression_cost = 0.0
        self.acres_burned = 0
        self.acres_crown_burned = 0

    def __repr__(self):
        """TODO"""
        return "A FireRecord object"
