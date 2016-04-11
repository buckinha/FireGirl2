import math
from utils.sigmoid import sigmoid

class GrowthModel:
    """TODO"""

    def __init__(self):
        self.VERBOSE = False

        #INITIALIZE GROWTH AND FUEL VECTORS
        #maximum age for volume and fuel accumulation
        self.max_age = 300
        #maximum site index
        self.max_si = 100

        #growth values are needed for each combination of ages and site indices
        self.PIPO_volumes = [ [self.growth_function_PIPO(age, si) for age in range(self.max_age)] for si in range(self.max_si) ]

        #Initialize fuel succession vectors
        #self.PIPO_ladder_fuels = [ self.ladder_fuel_function_PIPO(age) for age in range(self.max_age) ] 
        #self.PIPO_surface_fuels = [ self.surface_fuel_function_PIPO(age) for age in range(self.max_age) ] 


    def __repr__(self):
        """TODO"""
        return "FGGrowth.GrowthModel Object"

    def simulate_growth(self, FGPathway_object):
        """Simulates vegetation growth, according to the current settings, on a given FGPathway

        PARAMETERS
        ----------

        FGPathway_object
            The FGPathway object on which to simulate vegetation growth


        RETURNS
        -------
        None

        """
        pass


    #####################
    ## PRIMARY GETTERS ##
    #####################

    #get the qty of ladder fuels for a given species and fuel age
    def get_volume(self, age, site_index, species="DEFAULT"):
        """Looks up the timber volume per acre for a stand of the given age and site index"""

        #capping input values
        age = min(self.max_age-1, age)
        site_index = min(self.max_si-1, site_index)

        #forcing int types
        si = int(site_index)
        age = int(age)

        if (species == "DEFAULT") or (species == "PIPO"):
            return self.PIPO_volumes[si][age]
        else:
            if self.VERBOSE:
                print("Unknown species type in GrowthModel.get_volume()")
            return 0.0

    #get the qty of ladder fuels for a given species and fuel age
    def get_ladder_fuel(self, stand_age, years_since_fire, species="DEFAULT"):
        """Looks up the ladder fuel multiplier at the given age and site index

        This value will be compared against the weather-related fire spread rates
        to either increase or decrease chance of crown fire

        PARAMETERS
        ----------
        stand_age
            how many years has the stand been growing
        years_since_fire
            how many years since a fire. If this value is less than stand_age, that 
            indicates a surface fire has occured since stand initiation, and hense,
            ladder fuels may be reduced, depending on how long it has been

        RETURNS
        -------
        ladder_fuel_loading value to be used by an associated FireModel object
        """

        #capping input values
        age = int(min(self.max_age-1, stand_age))
        
        if (species == "DEFAULT") or (species == "PIPO"):
            return self.ladder_fuel_function_PIPO(stand_age, years_since_fire)
        else:
            if self.VERBOSE:
                print("Unknown species type in GrowthModel.get_ladder_fuel()")
            return 0.0

    #get the qty of surface fuels for a given species and fuel age
    def get_surface_fuel(self, fuel_age, stand_age, species="DEFAULT"):
        """Looks up the ladder fuel multiplier at the given age and site index

        This value will be compared against the weather-related fire spread rates
        to either increase or decrease surface spread rate
        """

        #capping input values
        age = int(min(self.max_age-1, age))
        
        if (species == "DEFAULT") or (species == "PIPO"):
            return self.surface_fuel_function_PIPO(self, fuel_age, stand_age)
        else:
            if self.VERBOSE:
                print("Unknown species type in GrowthModel.get_surface_fuel()")
            return 0.0


    #################################
    ## Primary Modelling Functions ##
    #################################

    def growth_function_PIPO(self, age, site_index):
        """The wood volume per acre of Pinus ponderosa given the stand age and site site_index

        Site index should be in meters (i.e. the expected tree height at 100 years)

        I fitted an approximation to a set of functions which themselves approximated volume growth given
        specific site indices. The individual site-index-specific functions are of the form v = a*ln(t) - b
        The parameters of those functions were model-able, so I did, and it gave:
            Volume =  (67.793*e^(0.04730*s)) * ln(t) - (201.18*e^(0.044199*s))

        These calculations were all on a per-hectare basis, so the function will finish by converting
        to cubic meters per acre.

        """
        #TESTED 3-15-16: This function recreates the input data acceptably
        if age == 0:
            return 0.0
        else:
            param_a = 67.793 * math.e**(0.04730*site_index)
            param_b = 201.18 * math.e**(0.044199*site_index)
            volume =  param_a * math.log(age) - param_b
            if volume < 0.0:
                return 0.0
            else:
                #this is in cubic meters per hectare; convert to per-acre
                volume = volume * 2.47105 #2.47105 acres per hectare
                return volume

    def surface_fuel_function_PIPO(self, fuel_age, stand_age):
        """The surface fuel value in a stand given the time since a fire.

        Returns a non-negative float, with a value of 1.0 reflecting "average"
        fuel loading, which corresponds to the average fire spread rates inherent 
        in the FWI calculation for weather-related spread rates.

        PARAMETERS
        ---------
        surface_fuel_age
            the number of years since the last fire (either surface OR stand-replacing)

        stand_age
            the number of years since the last stand-replacing fire or clear-cut, etc...

        RETURNS
        -------
        Fuel Loading value needed in the associated FireModel object.

        """
        

        #in the first several years after a clearcut/stand-replacing fire, there's a lot of
        #brush and downed woody debris. After this, it declines as trees fill in, hitting
        #a low around 20 yrs (???) and then increasing again as the understory re-initializes

        #if there's been a recent surface fire (not a stand replacing fire) then the surface
        #fuel loading will be temporily reduced, with full loading returning within 5 years
        # of the fire.

        #how quickly do fuels build up to max, after a clear-cut/stand-replacing fire
        fuel_greenup_years = 4

        #the lowest value of the fuel loading
        low_point_fuel_load = 0.5

        #the turning point age, where surface fuels stop declining and start to increase again
        age_for_increase = 20

        #how quickly does fuel load increase after the turning point age
        reinit_growth_rate = 0.2

        #maximum surface fuel loading in the long run
        max_LR_fuel_load = 1.3


        fuel_load = 1.0
        if stand_age < age_for_increase:
            fuel_load =  low_point_fuel_load + (1.0-low_point_fuel_load) / (age_for_increase - stand_age)
        else:
            _growing_age = stand_age - age_for_increase
            fuel_load = min( _growing_age * reinit_growth_rate,  max_LR_fuel_load)


        #now account for green-up after a surface fire
        surf_fire_mult = (1.0 / fuel_greenup_years) * min(fuel_age, fuel_greenup_years)

        return (fuel_load * surf_fire_mult)



    def ladder_fuel_function_PIPO(self, stand_age, years_since_fire):
        """The ladder fuel value in a stand given the time since a fire.

        In Pinus ponderosa stands,
        the historical fire regime which maintained old trees had return intervals from 1-30 years.
        With fire exclusion, the understory will begin to fill with shade tolerant species. They
        should start representing a threat of crown fire sometime after 30 years or so, to simulate
        this historical dynamic.



        """
        #lodgepole-style build-up pattern:
        #change parameter 'center' to adjust where fuel hits it's halfway point
        lodgepole_style_fuels = sigmoid(x=min(years_since_fire,stand_age), center=30, min_val=0.0, max_val=1.3)
        
        #in lodgepole, pretty much any fire is stand-replacing. In Ponderosa, after about age 20, 
        # stands are very resilient to fire. Surface fires then act to reduce ladder fuels and 
        # maintain the overstory

        #so here, instead of stand age, the years_since_fire value is used. As long as fires of some
        #kind are happening every 30 years or so, the ladder fuel value will never rise very high 
        # (in the case above, with center=30, max=1.3, at thirty years, the fuel_loading will be 0.65)

        return lodgepole_style_fuels

        

        

    