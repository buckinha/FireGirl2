import FGFire, FGHarvest, FGTreatments, FGGrowth, FGPolicy, FGWeather
import DiamondSquare as DS
import numpy as np
#import matplotlib.pyplot as plt


class FGPathway:
    """
    This is the primary FireGirl class. An instantiated FireGirlPathway object will hold
    all the data associated with a single FireGirl simulation, and all the methods
    needed to run that simulation.

    INITIALIZATION PARAMETERS
    -------------------------
    landscape_size, random_seed

    landscape_size
        An int or tuple/list/etc denoting the shape of the landscape. If an int is passed,
        the landscape will be a square with that value as the length of each side.

    random_seed
        A NUMERIC random number seed. FireGirl uses mathematical operations on this seed
        to make related seeds for each of its submodels. As long as it can be added, 
        multiplied, etc..., it should work fine.

    """


    def __init__(self, landscape_size=(129,129), random_seed=None):

        #maintenance flags
        self.VERBOSE = True
        self.DEBUGGING = True


        #primary simulation models
        self.FireModel = FGFire.SpreadModel()
        self.HarvestModel = FGHarvest.HarvestModel()
        self.TreatmentModel = FGTreatments.TreatmentModel()
        self.GrowthModel = FGGrowth.GrowthModel()
        self.WeatherModel = FGWeather.WeatherModel()


        #sanitize landscape_size
        #check if it's iterable, and of length 2
        if not hasattr(landscape_size,"__iter__"):
            #it's not iterable, so assume it's an int and correc that
            self.size = (landscape_size, landscape_size)
        else:
            #it's iterable, so save the first two values
            self.size = (landscape_size[0], landscape_size[1])


        #primary data arrays, etc...
        self.start_year_stand = np.zeros(self.size)
        self.start_year_surface_fuels = np.zeros(self.size)
        self.start_year_ladder_fuels = np.zeros(self.size)
        self.site_productivity = np.zeros(self.size)

        self.year_history = [] # a list to hold all of this simulation's YearRecord objects
        self.current_year = 0
        self.primary_random_seed = random_seed


    #adding a custom __repr__ method, esp. for use with ipython's '?' command
    def __repr__(self):
        """TODO"""
        return "FGPathway Object"


    def simulate(self, years):
        """Simulates a given number of years using the currently selected models.

        PARAMETERS
        ----------
        years
            The number of years to simulate, starting at the pathway's current year.

        RETURNS
        -------
        None
        """

        for y in range(years):
            self.do_fires()
            self.do_harvest()
            self.do_fuel_treatments()
            self.do_growth()
            self.current_year += 1



    def do_fires(self):
        """Uses the various components of the fire model to draw and (possibly) spread one year's fires.
        """

        ##########################################################
        # 1) Find out how many ignitions there are this year,
        #      and their associated weather streams/forecasts
        ##########################################################
        weather_seed = self.primary_random_seed + self.current_year
        weathers, forecasts = self.WeatherModel.get_new_fires(random_seed=weather_seed)

        #generate ignition locations
        locations = [ (random.uniform(self.size[0], self.size[1])) for i in range(len(weathers))]

        ### FOR EACH IGNITION THIS YEAR:
        for i in range(len(weathers)):
            #we can't get a list of suppression decisions all at once, because each fire
            # may change the landscape in the vicinity of the NEXT fire, and that may in
            # turn change the policy decision.

            ##########################################################
            # 2) Use the current suppression policy to make choices
            ##########################################################
            supr_decision = self.Policy.get_pol_decision(self, locations[i], forecasts[i])

            ##########################################################
            # 3) Simulate each fire (and potential suppression)
            ##########################################################
            self.FireModel.simulate_fire(self, locations[i], weathers[i], supr_decision)


    def do_harvest(self):
        """Uses the selected logging model to harvest one year's worth of timber.
        """
        self.HarvestModel.simulate_harvest(self)


    def do_fuel_treatments(self):
        """Uses the selected fuel treatment model to simulate treatments for one year."""
        self.TreatmentModel.simulate_treatments(self)


    def do_growth(self):
        """Uses the selected growth models to advance the vegetation on the landscape one year.
        """
        self.GrowthModel.simulate_growth(self)


    ###########################
    ### GETTERS and SETTERS ###
    ###########################
    def get_surface_fuel(self, loc):
        """Returns the surface fuel value for the given location"""
        s_fuel_age = self.current_year - self.start_year_surface_fuels[loc[0], loc[1]]
        return self.GrowthModel.get_surface_fuel(age=s_fuel_age,species="DEFAULT")

    def get_ladder_fuel(self, loc):
        """Returns the surface fuel value for the given location"""

        l_fuel_age = self.current_year - self.start_year_ladder_fuels[loc[0], loc[1]]
        return self.GrowthModel.get_ladder_fuel(age=l_fuel_age,species="DEFAULT")





class YearRecord:
    """Records information about a single simulation year."""

    def __init__(self):
        self.fire_history = [] #a list to hold any FireRecord objects associated with this year

        #yearly sums, averages, etc...
        self.fire_count = 0
        self.suppression_costs = 0.0
        self.acres_burned = 0
        self.acres_crown_burned = 0

        self.harvest_revenue = 0.0
        self.acres_harvested = 0


    def __repr__(self):
        """TODO"""
        return "A YearRecord object"




