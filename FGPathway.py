import FGFire, FGHarvest, FGTreatments, FGGrowth, FGPolicy


class FGPathway:
    """
    This is the primary FireGirl class. An instantiated FireGirlPathway object will hold
    all the data associated with a single FireGirl simulation, and all the methods
    needed to run that simulation.
    """


    def __init__(self):
        self.VERBOSE = True
        self.FireModel = FGFire.SpreadModel()
        self.HarvestModel = FGHarvest.HarvestModel()
        self.TreatmentModel = FGTreatments.TreatmentModel()
        self.GrowthModel = FGGrowth.GrowthModel()

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



    def do_fires(self):
        """Uses the various components of the fire model to draw and (possibly) spread one year's fires.
        """

        ##########################################################
        # 1) Find out how many ignitions there are this year
        ##########################################################
        ignitions = self.FireModel.get_new_ignitions(self)

        ### FOR EACH IGNITION THIS YEAR:
        for ign in ignitions:

            ##########################################################
            # 2) Use the current suppression policy to make choices
            ##########################################################
            supr_decision = self.Policy.get_pol_decision(ign)

            ##########################################################
            # 3) Simulate each fire (and potential suppression)
            ##########################################################
            self.FireModel.simulate_fire(self, ign, supr_decision)


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