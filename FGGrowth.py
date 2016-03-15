import math

class GrowthModel:
    """TODO"""

    def __init__(self):
        #Initialize growth curve vectors

        #Initialize fuel succession vectors
        pass

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



    #get the qty of ladder fuels for a given species and fuel age
    def get_ladder_fuel(age, species="DEFAULT"):
        """TODO"""
        return 1.0

    #get the qty of surface fuels for a given species and fuel age
    def get_surface_fuel(age, species="DEFAULT"):
        """I'm not sure I'm going to do much with surface fuels and spread rates"""
        return 1.0


    def growth_function_PIPO(age, site_index):
        """The wood volume per hectare(?) of Pinus ponderosa given the stand age and site site_index

        Site index should be in meters (i.e. the expected tree height at 100 years)

        I fitted an approximation to a set of functions which themselves approximated volume growth given
        specific site indices. The individual site-index-specific functions are of the form v = a*ln(t) - b
        The parameters of those functions were model-able, so I did, and it gave:
            Volume =  (67.793*e^(0.04730*s)) * ln(t) - (201.18*e^(0.044199*s))

        """
        #TESTED 3-15-16: This function recreates the input data acceptably
        param_a = 67.793 * math.e**(0.04730*site_index)
        param_b = 201.18 * math.e**(0.044199*site_index)
        volume =  param_a * math.log(age) - param_b
        return volume


    