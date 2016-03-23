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
        self.PIPO_ladder_fuels = [ self.ladder_fuel_function_PIPO(age) for age in range(self.max_age) ] 
        self.PIPO_surface_fuels = [ self.surface_fuel_function_PIPO(age) for age in range(self.max_age) ] 


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
        """Looks up the timber volume for a stand of the given age and site index"""

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
    def get_ladder_fuel(self, age, species="DEFAULT"):
        """Looks up the ladder fuel quantity (TODO: in what units?) at the given age and site index"""

        #capping input values
        age = int(min(self.max_age-1, age))
        
        if (species == "DEFAULT") or (species == "PIPO"):
            return self.PIPO_ladder_fuels[age]
        else:
            if self.VERBOSE:
                print("Unknown species type in GrowthModel.get_ladder_fuel()")
            return 0.0

    #get the qty of surface fuels for a given species and fuel age
    def get_surface_fuel(self, age, species="DEFAULT"):
        """I'm not sure I'm going to do much with surface fuels and spread rates"""

        #capping input values
        age = int(min(self.max_age-1, age))
        
        if (species == "DEFAULT") or (species == "PIPO"):
            return self.PIPO_surface_fuels[age]
        else:
            if self.VERBOSE:
                print("Unknown species type in GrowthModel.get_surface_fuel()")
            return 0.0


    #################################
    ## Primary Modelling Functions ##
    #################################

    def growth_function_PIPO(self, age, site_index):
        """The wood volume per hectare(?) of Pinus ponderosa given the stand age and site site_index

        Site index should be in meters (i.e. the expected tree height at 100 years)

        I fitted an approximation to a set of functions which themselves approximated volume growth given
        specific site indices. The individual site-index-specific functions are of the form v = a*ln(t) - b
        The parameters of those functions were model-able, so I did, and it gave:
            Volume =  (67.793*e^(0.04730*s)) * ln(t) - (201.18*e^(0.044199*s))

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
                return volume

    def surface_fuel_function_PIPO(self, surface_fuel_age):
        """The surface fuel value in a stand given the time since a fire.

        For now, units are 0-100, reflecting a generic none-to-maximum range.

        Currently defaults to a constant value of 50
        """
        return 50.0

    def ladder_fuel_function_PIPO(self, ladder_fuel_age):
        """The ladder fuel value in a stand given the time since a fire.

        For now, units are 0-100, reflecting a generic none-to-maximum range.

        Ladder fuels will accumulate according to a sigmoid function. In Pinus ponderosa stands,
        the historical fire regime which maintained old trees had return intervals from 1-30 years.
        With fire exclusion, the understory will begin to fill with shade tolerant species. They
        should start representing a threat of crown fire sometime after 30 years or so, to simulate
        this historical dynamic.

        """
        #change parameter 'center' to adjust where fuel hits 50
        return sigmoid(x=ladder_fuel_age, center=25, min_val=0, max_val=100)

        

        

    