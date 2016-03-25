

class HarvestModel:
    """TODO"""

    def __init__(self):
        #how many stands should be left un-cut between each stand which is cut
        self.selection_cut_gap = 3

        #largest clear-cut size allowed
        self.clear_cut_size_limit = 10

        #the rotation age for stands in this forest
        self.rotation_age = 55 #years

        #how many cells/acres can be harvested in one year
        self.annual_harvest_acres_cap = float("inf")

        #timber price
        # 1million boardfeet = 2359.737 cubic meters
        # with $25/mbf, that makes $25/2360m^3
        # which is $0.01059322 per cubic meter
        self.dollars_per_cubic_meter = 0.01059322


    def __repr__(self):
        """TODO"""
        return "FGHarvest.HarvestModel Object"


    def simulate_harvest(self, FGPathway_object, method="selection"):
        """Simulates harvesting, according to the current settings, on a given FGPathway

        PARAMETERS
        ----------
        FGPathway_object
            The FGPathway object on which to simulate harvesting
        method
            Set to either "selection" or "clear cut". Choosing 'selection' sets the harvest 
            model to try to cut only single, isolated cells (the smallest unit it can cut).
            Choosign "clear cut" sets the harvest model to try to cut large blocks of cells
            at a time, up to a maximum size, held in HarvestModel.clear_cut_size_limit


        RETURNS
        -------
        a dictionary containing the harvest summary. Keys are:
            "Acres Cut", "Volume Cut", "Revenue"

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
        -------
        a dictionary containing the harvest summary. Keys are:
            "Acres Cut", "Volume Cut", "Revenue"
        """
        pw = FGPathway_object

        acres_cut = 0
        volume_cut = 0

        x_width = pw.size[0]
        y_width = pw.size[1]

        #loop over all stands and cut up to this year's max volume of harvestable-aged trees
        for outer in range(self.selection_cut_gap):
            if volume_cut > self.annual_harvest_cap: break

            for i in range(outer, x_width, self.selection_cut_gap):
                if volume_cut > self.annual_harvest_cap: break

                for j in range(0, y_width, self.selection_cut_gap):
                    if volume_cut > self.annual_harvest_cap: break

                    #if this cell/stand is of harvestable age, cut it and record the timber volume and acres
                    if  pw.get_age([i,j]) > self.rotation_age:
                        #it's harvestable, so cut it.
                        acres_cut += pw.acres_per_cell
                        volume_cut += pw.get_volume([i,j])
                        self.cut_stand(pw, [i,j])

        summary = {"Acres Cut":acres_cut,
                   "Volume Cut":volume_cut,
                   "Revenue": self.get_revenue(volume_cut)}

        return summary


    def clear_cut(self, FGPathway_object):
        """
        A clear cut system will select relatively even age, adjacent stands for cutting in large groups,
        up to some maximum allowed size

        RETURNS
        -------
        a dictionary containing the harvest summary. Keys are:
            "Acres Cut", "Volume Cut", "Revenue"
        """

        #TODO

        acres_cut = 0
        volume_cut = 0

        summary = {"Acres Cut":acres_cut,
                   "Volume Cut":volume_cut,
                   "Revenue": self.get_revenue(volume_cut)}
                   
        return summary


    def cut_stand(self, FGPathway_object, loc):
        """Cuts a stand at this location"""
        FGPathway_object.stand_init_yr[loc[0],loc[1]] = FGPathway_object.current_year

        #TODO
        #set slash accumulation
        #burning slash and remaining vegetation?


    def get_revenue(self, volume):
        return volume * self.dollars_per_cubic_meter


    def set_dollars_per_mbf(self, dollars_per_mbf):
        """sets the harvest model's stumpage value"""
        # 1million boardfeet = 2359.737 cubic meters
        #
        #so, for example:
        # with $25/mbf, that makes $25/2360m^3
        # which is $0.01059322 per cubic meter

        self.dollars_per_cubic_meter = dollars_per_mbf / 2359.737

