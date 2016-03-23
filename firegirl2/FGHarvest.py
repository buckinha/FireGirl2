

class HarvestModel:
    """TODO"""

    def __init__(self):
        #how many stands should be left un-cut between each stand which is cut
        self.selection_cut_gap = 3

        #largest clear-cut size allowed
        self.clear_cut_size_limit = 10


    def __repr__(self):
        """TODO"""
        return "FGHarvest.HarvestModel Object"


    def simulate_harvest(self, FGPathway_object, method="selection"):
        """Simulates harvesting, according to the current settings, on a given FGPathway



        PARAMETERS
        ----------

        FGPathway_object
            The FGPathway object on which to simulate harvesting


        RETURNS
        -------
        None

        """
        
        if method == "selection":
            summary_vals = self.selection_cut(FGPathway_object)
        elif method == "clear cut":
            summary_vals = self.clear_cut(FGPathway_object)

        return summary_vals


    def selection_cut(self, FGPathway_object):
        """
        For a selection or group-selection cut system, trees of harvestable age are cut in small
        patches (or individual trees) and the remaining young trees are left to grow. In the 
        simulator, the very smallest unit of cut which is possible is a single cell. The selection-cut
        algorithm will try to encapsulate this behavior by selecting only individual cells, and 
        where possible, leaving an un-cut seperation between them

        RETURNS
        (acres_cut, revenue)
        """



    def clear_cut(self, FGPathway_object):
        """
        A clear cut system will select relatively even age, adjacent stands for cutting in large groups,
        up to some maximum allowed size

        RETURNS
        (acres_cut, revenue)
        """