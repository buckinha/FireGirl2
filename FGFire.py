import random, Queue, math
import numpy as np

USING_8_ANGLE_WIND = True

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
        for ign in init_ignitions:
            #check to see if any of the spread rates are greater than zero.
            if ign[0] > 0:
            spreading = True
            break

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
            current_ign = pq.get()
            loc = (current_ign[1], current_ign[2])

            #increment current time to this cell's ignition time. This can allow a single
            # ignition to go beyond the max time.
            current_time = current_ign[0]
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
            for ign in n_igns:
                #if the spread rate is other than zero
                if ign[0] > 0:
                    pq.put(ign)


        #all done with the queue, so either we ran out of new cells, or the time expired
        fr = FireRecord()
        fr.acres_burned = cells_burned
        fr.acres_crown_burned = cells_crowned
        fr.weather = weather[:]
        fr.suppressed = sppr_dec
        fr.ignition_location = location[:]

        fr.suppression_cost = calc_suppression_cost(fr)

        return fr


def calc_spread_rate(FGPathway_object, location, weather_today, supr_dec):
    """Calculates the spread rate at this location, given the weather.

    RETURNS
    -------
    spread_rate
        float, in units of "acre-length"/day = 208ft/day 
    """


    #### OLD METHOD from FireGirl v1 ### 
    def OLDcalcFireSpreadRate(wind, temp, fuel):
        #This function calculates the logistic function that governs fire spread
        #   rates. The parameters below are arbitrary, and give rise to the
        #   shape I wanted for the model:

        ### Variables from the old FireGirl v1 initialization ### ### ### ### 
        #These are the parameters that give shape to the fire spreadrate calculation
        # It is a logistic function that takes FireGirl's (windspeed + temperature)
        # as it's input.
        fire_param_inputscale = 10
        fire_param_outputscale = 10
        fire_param_zeroadjust = 15
        fire_param_smoothness = 0.4
        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
        
        out_scale = fire_param_outputscale
        in_scale = fire_param_inputscale
        zero_adj = fire_param_zeroadjust
        smooth = fire_param_smoothness
        
        exponent = (   -1 * smooth *     (   ((wind + temp + fuel) / in_scale) - zero_adj   )       )
        fspread = out_scale / (1 + math.exp(exponent))
        
        #Enforcing minimum spread restrictions
        if (wind + temp) < self.min_spread_windtemp:
            fspread = 0
        if fuel < self.min_spread_fuel:
            fspread = 0
        
        return fspread

    #using old model
    wind = weather_today["Wind Speed"]
    temp = weather_today["Temperature"]
    fuel = FGPathway_object.get_surface_fuel(location)
    sr = OLDcalcFireSpreadRate(wind, temp, fuel)

    return sr

    

def calc_suppression_cost(fire_record):
    return 0.0

def get_neighbor_ignitions(FGPathway_object, location, weather_today, supr_dec):
    """ Calculates when (if ever) each neighbor will ignite.

    RETURNS
    A list of ignitions, [ (ignition_time, location_x, location_y), (...), ... , (...) ]
    """

    #calculate the forward spreadrate given the wind speed and fuels
    """TODO"""
    sprd_rt = calc_spread_rate(FGPathway_object, location, weather_today, supr_dec)
    #ENFORCE sprd_rt > 0
    if sprd_rt <= 0:
        return []
    
    #get the length-to-width ratio associated with this spread rate
    l_w_r = calc_l_w_ratio(weather_today["Wind Speed"])

    #the angle to each cell
    #TODO: these don't need to be calculated every time. Pre-compute them
    cell_angle = np.asarray([i * np.pi/4.0 for i in range(8)])

    #the angle to each cell in terms of the ellipse's primary axis
    ell_angle = cell_angle - np.radians(weather_today["Wind Direction"])

    #the multiplier for spread rate, based on the ellipse
    sp_rt_mult = []
    if USING_8_ANGLE_WIND:
        sp_rt_mult = np.asarray([ellipse_dist_poly(t, l_w_r) for t in ell_angle])
    else:
        sp_rt_mult = np.asarray([ellipse_dist_ratio(t, l_w_r) for t in ell_angle])

    #distance to each cell
    distances = np.asarray([ 1.0, 1.4142, 1.0, 1.4142, 1.0, 1.4142, 1.0, 1.4142 ])

    #use spread rate, multipliers and distances to compute ignition times of each neighbor
    spread_rates = sprd_rt * sp_rt_mult
    #element-wise division
    ignition_times = np.divide(distances,spread_rates)

    #create the return list
    #Note, these are not parsed to get rid of infinite, 0, or other strange ignition times
    final_list = [[ignition_times[0], location[0] + 1, location[1] + 0],
                  [ignition_times[1], location[0] + 1, location[1] - 1],
                  [ignition_times[2], location[0] + 0, location[1] - 1],
                  [ignition_times[3], location[0] - 1, location[1] - 1],
                  [ignition_times[4], location[0] - 1, location[1] + 0],
                  [ignition_times[5], location[0] - 1, location[1] + 1],
                  [ignition_times[6], location[0] + 0, location[1] + 1],
                  [ignition_times[7], location[0] + 1, location[1] + 1]]

    return final_list


#given a spread rate, calculates the fire ellipes l/w ratio
def calc_l_w_ratio(wind_speed):
    """From  "Development and Structure of the Canadian Forest Fire Behavior Prediction System"
    the equation used to compute the length-to-width ratio of the ellipse is:

        l_to_w = 1.0 + 8.729*(1.0-math.exp(-0.03*w))**2.155

    to nip off some computation time, I'm taking a linear approximation of this:

        l_to_w_aprx = 1.10993 + 0.0878841*w

    which has an R**2 fit value of 0.985 and a p-value for the regression of 4.6496e-77 

    the average execution times are 720ns and 260ns, respectively.

    The linear approximation will slightly over-estimate length-to-width for winds between 0 and 22kph
    and slightly overestimate afteward, until windspeeds are over ~80kph.

    PARAMETERS
    ----------
    wind_speed: wind speed in kph

    RETURNS
    -------
    float, indicating the length-to-width ratio of the fire footprint ellipse.
    """

    #limiting to values between 1 and 10
    if wind_speed < 0.0
        return 1.0
    else:
        return 1.10993 + 0.0878841*wind_speed

        #to convert mph to kph, multiply by 1.60934449789. This changes the equation to
        #return 1.10993 + 0.0878841*(1.60934449789*wind_speed)
        # or, simplified:
        #return 1.10993 + 0.14143579278*wind_speed

        #to convert m/s to kph, multiply by 3.6. This changes the equation to
        #return 1.10993 + 0.0878841*(3.6*wind_speed)
        # or, simplified:
        #return 1.10993 + 0.31638276*wind_speed



#calculations for the distance from an ignition point to the edge of the fire ellipse
def ellipse_dist_poly(theta, s):
    """This calculation takes an s value which is in proportion to the value of b being 1

    Rounds theta to the closest increment of 45, and then computes the corresponding polynomial
    model of that angle.

    PARAMETERS
    ----------
    theta: the angle away from "forward" at which the distance from the ignition to the edge should
        be calculated.
    l_w_ratio: the length-to-width ratio of the ellipse. 
        Needs to be a value no less than 1, and preferably less than 10

    """
    s = float(s)
    t = abs(int(4.0*theta/np.pi))
    if (t == 0) or (t == 8):
        #forward = s
        return s
    elif (t == 1) or (t == 7):
        diag = 0.84297641*s + 0.0970053613
        return diag
    elif (t == 2) or (t == 6):
        up = 0.0090215318*s**2 + 0.3691489777*s + 0.5191455988
        return up
    elif (t == 3) or (t == 5):
        back_diag = -0.0002197225*s**5 + 0.006687039*s**4 + -0.0788194038*s**3 + 0.4531392746*s**2 + -1.1664715313*s + 1.7741439645
        return back_diag
    elif t == 4:
        back = (1.0/s)
        return back
    else:
        #hmmm... TODO
        return 0.0

#calculation of any angle, given a length-to-width ratio
def ellipse_dist(theta, s):
    """This calculation takes an s value which is in proportion to the value of b being 1

    PARAMETERS
    ----------
    theta: the angle away from "forward" at which the distance from the ignition to the edge should
        be calculated.
    s: the proportional forward spread rate of the fire when b = 1
    
    """
    s = float(s)
    
    a = (s + 1.0/s) * 0.5

    b = 1.0
    
    x = a * math.cos(theta) + a - (1.0/s)

    y = b * math.sin(theta)

    dist = math.sqrt(x**2 + y**2)

    return dist

def ellipse_dist_ratio(theta, lwr):
    """ The ratio of the distance along angle theta to the foreward spreading distance

    PARAMETERS
    ----------
    theta: the angle away from "forward" in radians
    lwr: the length-to-width ratio of the ellipse

    RETURNS
    -------
    float: the ratio of the distances

    """

    """Clearer calculations:
    #set b=1, which makes a = lwr
    a = lwr
    b = 1.0

    #calculate f
    f = math.sqrt(a**2 - b**2)

    #get the distance from the focus to the edge, along angle theta
    dist = math.sqrt(  (a * math.cos(theta) + f)**2   + (b*math.sin(theta))**2  )

    #calculate the forward spread rate "distance" and compute the ratio
    s = a + f
    ratio = dist / s

    return ratio
    """
    #slightly faster version:
    # (PASSED RANDOM TESTING for being the same calculation)
    f = math.sqrt(lwr**2 - 1.0)
    dist = math.sqrt(  (lwr * math.cos(theta) + f)**2   + (math.sin(theta))**2  )
    return dist / (lwr + f)


def get_crown_burn(FGPathway_object, loc, weather_today, sppr_dec):
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
