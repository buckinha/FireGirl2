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


        #important pathway values
        self.year_history = [] # a list to hold all of this simulation's YearRecord objects
        self.current_year = 0
        self.primary_random_seed = random_seed


        #Primary data arrays, etc...
        #   site index: this remains constant
        self.site_index = DS.diamond_square(self.size, min_height=0, max_height=100, roughness=0.5, random_seed=random_seed, AS_NP_ARRAY=True).astype(int)
        #   each cell's stand initiation year: each one started in the last 100 years or so
        self.stand_init_yr = DS.diamond_square(self.size, min_height=-100, max_height=0, roughness=0.75, random_seed=random_seed+1, AS_NP_ARRAY=True)
        #   the last year in which each cell experienced a stand-replacing fire, leaving dead trees standing
        self.stand_rplc_fire_yr = DS.diamond_square(self.size, min_height=-100, max_height=0, roughness=0.75, random_seed=random_seed+2, AS_NP_ARRAY=True)
        #   the last year in which there was a surface fire
        self.surf_fire_yr = DS.diamond_square(self.size, min_height=-100, max_height=0, roughness=0.75, random_seed=random_seed+2, AS_NP_ARRAY=True)

        


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
            #new YearRecord object for this year
            yr = YearRecord()

            #simulate and record
            #note: the do___ methods will also update the pathway object
            yr.update_fire( self.do_fires() )
            yr.update_harvest( self.do_harvest() )
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

        #set up fire record object list
        fire_records = [None] * len(weathers)

        ### FOR EACH IGNITION THIS YEAR:
        for i in range(len(weathers)):
            #we can't get a list of suppression decisions all at once, because each fire
            # may change the landscape in the vicinity of the NEXT fire, and that may in
            # turn change the policy decision.

            ##########################################################
            # 2) Use the current suppression policy to make choices
            ##########################################################
            supr_decision = self.Policy.get_pol_decisions(self, locations[i], forecasts[i])

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
        self.fire_records = []

        self.harvest_revenue = 0.0
        self.acres_harvested = 0


    def __repr__(self):
        """TODO"""
        return "A YearRecord object"


    def update_harvest(values_from_harvest_model):
        """
        FGHarvest.HarvestModel.simulate_harvest() method returns a tuple: (acres_cut, revenue)
        """
        self.acres_harvested = values_from_harvest_model[0]
        self.harvest_revenue = values_from_harvest_model[1]


    def update_fire(fire_records):
        """Takes a list of fire records and updates values accordingly"""
        self.fire_records = fire_records
        for fr in fire_records:
            self.fire_count += 1
            self.suppression_costs += fr.suppression_cost
            self.acres_burned += fr.acres_burned
            self.acres_crown_burned += fr.acres_crown_burned