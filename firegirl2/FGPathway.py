import FGFire, FGHarvest, FGTreatments, FGGrowth, FGPolicy, FGWeather
import utils.DiamondSquare as DS
from utils.seed_add import seed_add as seed_add
import numpy as np
import random
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

        #fire suppression policy
        self.Policy = FGPolicy.SuppressionPolicy()

        #sanitize landscape_size
        #check if it's iterable, and of length 2
        if not hasattr(landscape_size,"__iter__"):
            #it's not iterable, so assume it's an int and correc that
            self.size = (landscape_size, landscape_size)
        else:
            #it's iterable, so save the first two values
            self.size = (landscape_size[0], landscape_size[1])


        #important pathway values
        self.year_history = [] # a list to hold all of this simulation's YearRecord objects
        self.current_year = 0
        self.primary_random_seed = random_seed


        #Primary data arrays, etc...
        #   site index: this remains constant
        self.site_index = DS.diamond_square(self.size, min_height=0, max_height=100, roughness=0.5, random_seed=seed_add(self.primary_random_seed, 0),AS_NP_ARRAY=True).astype(int)
        #   each cell's stand initiation year: each one started in the last 100 years or so
        self.stand_init_yr = DS.diamond_square(self.size, min_height=-100, max_height=0, roughness=0.75, random_seed=seed_add(self.primary_random_seed, 1), AS_NP_ARRAY=True).astype(int)
        #   the last year in which each cell experienced a stand-replacing fire, leaving dead trees standing
        self.stand_rplc_fire_yr = DS.diamond_square(self.size, min_height=-100, max_height=0, roughness=0.75, random_seed=seed_add(self.primary_random_seed, 2), AS_NP_ARRAY=True).astype(int)
        #   the last year in which there was a surface fire
        self.surf_fire_yr = DS.diamond_square(self.size, min_height=-100, max_height=0, roughness=0.75, random_seed=seed_add(self.primary_random_seed, 2), AS_NP_ARRAY=True).astype(int)


        #units
        #how many acres per cell?
        self.acres_per_cell = 25


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

        #creat new year records for this simulation
        year_records = [ YearRecord(i) for i in range(self.current_year, self.current_year+years) ]

        for yr in year_records:
            #simulate and record
            #note: the do___ methods will also update the pathway object itself
            yr.update_fire( self.do_fires() )
            yr.update_harvest( self.do_harvest() )
            #self.do_fuel_treatments()
            #self.do_growth()
            self.current_year += 1

        #add the new records to the ongoing history
        self.year_history = self.year_history + year_records

    def do_fires(self):
        """Uses the various components of the fire model to draw and (possibly) spread one year's fires.
        """

        ##########################################################
        # 1) Find out how many ignitions there are this year,
        #      and their associated weather streams/forecasts
        ##########################################################
        weather_seed = seed_add(self.primary_random_seed, self.current_year)
        weather_seed = seed_add(weather_seed, 298238234)
        
        weathers, forecasts = self.WeatherModel.get_new_fires(random_seed=weather_seed)
        
        #if there are no fires this year, return nothing
        if len(weathers) == 0:
            return []

        #generate ignition locations
        def _rand_loc(i):
            random.seed(seed_add(weather_seed, i+253456))
            _x = random.uniform(self.size[0], self.size[1])
            _y = random.uniform(self.size[0], self.size[1])
            return (_x, _y)

        locations = [ _rand_loc(i) for i in range(len(weathers))  ]

        #set up fire record object list
        fire_records = [None] * len(weathers)

        ### FOR EACH IGNITION THIS YEAR:
        for i in range(len(weathers)):
            #we can't get a list of suppression decisions all at once, because each fire
            # may change the landscape in the vicinity of the NEXT fire, and that may in
            # turn change the policy decision. So we have to do one at a time and 
            # simulate the fire, before getting the next decision

            ##########################################################
            # 2) Use the current suppression policy to make choices
            ##########################################################
            supr_decision = self.Policy.get_decision(self, locations[i], forecasts[i])

            ##########################################################
            # 3) Simulate each fire (and potential suppression)
            ##########################################################
            fire_records[i] = self.FireModel.simulate_fire(self, locations[i], weathers[i], supr_decision) 

        return fire_records


    def do_harvest(self):
        """Uses the selected logging model to harvest one year's worth of timber.
        """
        summary_vals = self.HarvestModel.simulate_harvest(self, method="selection")
        return summary_vals


    def do_fuel_treatments(self):
        """Uses the selected fuel treatment model to simulate treatments for one year."""
        summary_vals = self.TreatmentModel.simulate_treatments(self)
        return summary_vals


    def do_growth(self):
        """Uses the selected growth models to advance the vegetation on the landscape one year.
        """
        pass
        #self.GrowthModel.simulate_growth(self)


    ###########################
    ### GETTERS and SETTERS ###
    ###########################
    def get_surface_fuel(self, loc):
        """Returns the surface fuel value for the given location"""

        #Growth model method signature is: 
        #def get_surface_fuel(self, stand_age, fuel_age, species="DEFAULT")
        surf_fuel_age = self.current_year - self.surf_fire_yr[loc[0], loc[1]]
        return self.GrowthModel.get_surface_fuel(stand_age=self.get_age(loc), fuel_age=surf_fuel_age, species="DEFAULT")

    def get_ladder_fuel(self, loc):
        """Returns the surface fuel value for the given location

        This value will be used by the FireModel to calculate spread rates and crown fires. 
        In the default models, it is a non-negative multiplier to be used on the weather-
        related spread rate calculations; typically with values between 0.5 and 1.3 or so.
        """

        #GrowthModel method signature is:
        # def get_ladder_fuel(self, stand_age, years_since_fire, species="DEFAULT")

        return self.GrowthModel.get_ladder_fuel(stand_age=self.get_age(loc), years_since_fire=self.get_years_since_fire(loc) )

    def get_volume(self, loc):
        """Gets the wood volume of the trees in a stand"""
        age = self.get_age(loc)
        si = self.site_index[loc[0]][loc[1]]

        #volume from the volume model
        vol_per_acre = self.GrowthModel.get_volume(age=age, site_index=si)

        #volume per cell
        vol_cell = vol_per_acre * self.acres_per_cell

        return vol_cell

    def get_age(self, loc):
        """The age of the current stand"""
        return self.current_year - self.stand_init_yr[loc[0]][loc[1]]

    def get_years_since_fire(self, loc):
        """For a given location, how many years have passed since ANY fire"""
        ladder_fuel_age = self.current_year - self.stand_rplc_fire_yr[loc[0], loc[1]]
        surf_fuel_age = self.current_year - self.surf_fire_yr[loc[0], loc[1]]
        return min( ladder_fuel_age, surf_fuel_age)



class YearRecord:
    """Records information about a single simulation year.

    INSTANTIATION PARAMETERS
    year: an integer year which this YearRecord object is holding values for
    path: OPTIONAL. When multiple runs are done on the same landscape (Monte
        Carlo sims, for example), path_number can hold a value to identify 
        which run this record belongs to.

    """

    def __init__(self, year, path_number=-1):
        #the current year, which this object records
        self.year = year
        self.path = path_number

        #a list to hold any FireRecord objects associated with this year
        self.fire_history = [] 

        #yearly sums, averages, etc...
        self.fire_count = 0
        self.suppression_costs = 0.0
        self.acres_burned = 0
        self.acres_crown_burned = 0
        self.fire_records = []

        self.harvest_revenue = 0.0
        self.acres_harvested = 0
        self.volume_harvested = 0.0


    def __repr__(self):
        """TODO"""
        return "A FireGirl2 YearRecord object"


    def update_harvest(self, values_from_harvest_model):
        """
        FGHarvest.HarvestModel.simulate_harvest() method returns a tuple: (acres_cut, revenue)
        """
        self.acres_harvested = values_from_harvest_model["Acres Cut"]
        self.volume_harvested = values_from_harvest_model["Volume Cut"]
        self.harvest_revenue = values_from_harvest_model["Revenue"]


    def update_fire(self, fire_records):
        """Takes a list of fire records and updates values accordingly"""
        self.fire_records = fire_records
        for fr in fire_records:
            self.fire_count += 1
            self.suppression_costs += fr.suppression_cost
            self.acres_burned += fr.acres_burned
            self.acres_crown_burned += fr.acres_crown_burned