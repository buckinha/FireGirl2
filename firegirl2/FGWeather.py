#firegirl2/FGWeather.py
#FireGirl Weather Model

import utils.FWIFunctions as FWI
import random
import math

class WeatherModel:
    """Model for producing weather streams and weather forecasts for FireGirl2"""

    def __init__(self):
        self.forecast_accuracy = 0.8

    def __repr__(self):
        """TODO"""
        return "A FireGirl2 WeatherModel object"


    def get_new_fire_weather(self, date, random_seed=None):
        """Creates a new weather stream and forcast

        PARAMETERS
        ----------
        date
            the integer date of the year

        random_seed
            Any numeric value for seeding the weather/forecast generation process.
            Ensures replicability.

        RETURNS
        -------
        weather, forecast
        
        weather 
            A list of dictionaries of weather variables with the primary index being day.
        forcast
            The associated weather forcast, of identical form/shape as "weather"

        """

        #how many days long is this fire event?
        ave_fire_weather_days = 3
        random.seed(seed_add(random_seed, 3789284))
        day_count = int(random.expovariate(1.0/ave_fire_weather_days))

        #if the fire event is less than three days long, we'll need to add some extras to make sure
        #that at least the FORECAST is three days long
        extra_forecast_days = 3 - day_count

        #add days for the lead-in time, which is needed to allow FWI index values to come 
        # to equilibrium
        buffer_days = 10
        day_count += (buffer_days + extra_forecast_days)

        #get random weather variables for the days
        weather = [ self.draw_weather_variables(date, seed_add(random_seed, 9472843)) for i in range(day_count) ]
        forecast = weather[:]

        #now do a blending of the variables, walking forward from the first day, where
        # each day is a combination of (mostly) the previous day's value, and (somewhat)
        # it's own value
        w_blend = 0.8
        f_blend = self.forecast_accuracy * w_blend

        for i in range(1,day_count):
            weather[i]["Temperature"]    = w_blend * weather[i-1]["Temperature"]    + (1-w_blend) * weather[i]["Temperature"]
            weather[i]["RH"]             = w_blend * weather[i-1]["RH"]             + (1-w_blend) * weather[i]["RH"]
            weather[i]["Wind Speed"]     = w_blend * weather[i-1]["Wind Speed"]     + (1-w_blend) * weather[i]["Wind Speed"]
            weather[i]["Wind Direction"] = w_blend * weather[i-1]["Wind Direction"] + (1-w_blend) * weather[i]["Wind Direction"]
            weather[i]["Rainfall"]       = w_blend * weather[i-1]["Rainfall"]       + (1-w_blend) * weather[i]["Rainfall"]

            forecast[i]["Temperature"]    = f_blend * forecast[i-1]["Temperature"]    + (1-f_blend) * forecast[i]["Temperature"]
            forecast[i]["RH"]             = f_blend * forecast[i-1]["RH"]             + (1-f_blend) * forecast[i]["RH"]
            forecast[i]["Wind Speed"]     = f_blend * forecast[i-1]["Wind Speed"]     + (1-f_blend) * forecast[i]["Wind Speed"]
            forecast[i]["Wind Direction"] = f_blend * forecast[i-1]["Wind Direction"] + (1-f_blend) * forecast[i]["Wind Direction"]
            forecast[i]["Rainfall"]       = f_blend * forecast[i-1]["Rainfall"]       + (1-f_blend) * forecast[i]["Rainfall"]

        #now add the FWI variables
        #The first day will get a value of 50 for FFMC, DMC, and DC (moisture and drought codes)
        #After that, they will adjust themselves as they go
        weather[0]["FFMC"] = 50
        weather[0]["DMC"] = 50
        weather[0]["DC"] = 50
        forecast[0]["FFMC"] = 50
        forecast[0]["DMC"] = 50
        forecast[0]["DC"] = 50
        for i in range(1,day_count):
            #I'm holding the month to whatever it was when the fire started to avoid any 
            # discontinuities partway through a weather stream. Hense 'weather[0]["Date"]'
            MONTH = self.get_month(weather[0]["Date"]) 
            LAT = 45
            TEMP = weather[i]["Temperature"]
            RH = weather[i]["RH"]
            WIND = weather[i]["Wind Speed"]
            RAIN = weather[i]["Rainfall"]
            FFMCPrev = weather[i-1]["FFMC"]
            DMCPrev = weather[i-1]["DMC"]
            DCPrev = weather[i-1]["DC"]
            weather[i]["FFMC"] = FWI.FFMC(TEMP,RH,WIND,RAIN,FFMCPrev)
            weather[i]["DMC"] = (TEMP,RH,RAIN,DMCPrev,LAT,MONTH)
            weather[i]["DC"] = FWI.DC(TEMP,RH,RAIN,DMCPrev,LAT,MONTH)
            weather[i]["FWI"] = FWI.calcFWI(MONTH,TEMP,RH,WIND,RAIN,FFMCPrev,DMCPrev,DCPrev,LAT)

            TEMP = forecast[i]["Temperature"]
            RH = forecast[i]["RH"]
            WIND = forecast[i]["Wind Speed"]
            RAIN = forecast[i]["Rainfall"]
            FFMCPrev = forecast[i-1]["FFMC"]
            DMCPrev = forecast[i-1]["DMC"]
            DCPrev = forecast[i-1]["DC"]
            forecast[i]["FFMC"] = FWI.FFMC(TEMP,RH,WIND,RAIN,FFMCPrev)
            forecast[i]["DMC"] = (TEMP,RH,RAIN,DMCPrev,LAT,MONTH)
            forecast[i]["DC"] = FWI.DC(TEMP,RH,RAIN,DMCPrev,LAT,MONTH)
            forecast[i]["FWI"] = FWI.calcFWI(MONTH,TEMP,RH,WIND,RAIN,FFMCPrev,DMCPrev,DCPrev,LAT)

        #the forecast will always be three days long
        forecast = weather[buffer_days:buffer_days+3]

        #trim off the ten lead-in days
        weather = weather[buffer_days:]
        #trim off any extra forecast days
        if extra_forecast_days > 0:
            weather = weather[:-1*extra_forecast_days]

        return weather, forecast

    def get_new_fires(self, random_seed=None):
        """Generates a new series of fires for a simulation year and returns any/all of them

        PARAMETERS
        ----------
        random_seed
            Any numeric value for seeding the weather/forecast generation process.
            Ensures replicability.


        RETURNS
        -------
        weather_streams, forecasts

        weather_streams
            A list of weather streams. Each weather stream is a 2-d list, indexed by day,
            of a particular fire/weather event.

        forecasts
            A list of weather forecasts. Each forecast is a a 2-d list, indexed by day, of
            weather forecast information for a particular fire/weather event.

        """
        #how many fires are there this year?
        ave_fire_count = 0.5
        random.seed(seed_add(random_seed, 471294932))
        fire_count = int(random.expovariate(1.0 / ave_fire_count))

        
        weather_streams = [None]*fire_count
        forecasts = [None]*fire_count
        for f in range(fire_count):
            #drawing fire days bewteen April-ish and October-ish
            streams = self.get_new_fire_weather( date=random.randint(100,310), random_seed=seed_add(random_seed,128439322))
            weather_streams[i] = streams[0]
            forecasts[i] = streams[1]

        return weather_streams, forecasts


    def draw_weather_variables(self, date, random_seed=None):
        """Draws random weather variables given the integer date"""
        wind = self.draw_wind(date, random_seed)
        wind_dir = self.draw_wind_direction(date, random_seed)
        temp = self.draw_temp(date, random_seed)
        rh = self.draw_RH(date, random_seed)
        rain = self.draw_rain(date, random_seed)

        return {"Temperature":temp,
                "Wind Speed":wind,
                "Wind Direction":wind_dir,
                "RH":rh,
                "Rainfall":rain,
                "Date":date}

    def draw_wind(self, date, random_seed=None):
        """Random wind speed in kph

        Drawing from an exponential distribution with mean = 10
        TODO: what SHOULD it be?
        """
        wind_mean = 10
        random.seed(seed_add(random_seed,439201))
        return random.expovariate(1.0 / wind_mean)

    def draw_wind_direction(self, date, random_seed=None):
        """A purely random wind direction, in degrees from North"""
        random.seed(seed_add(random_seed, 818127))
        return random.uniform(0,364)
        
    def draw_temp(self, date, random_seed=None):
        """Random temperature for the given date (as day of year)"""

        # from http://www.na.fs.fed.us/spfo/pubs/silvics_manual/Volume_1/pinus/ponderosa.htm
        # average annual temperatures are between 5 and 10 C (41 and 50 F), 
        # and average July-August temperatures are between 17 and 21 C
        # Annual extremes are from -40 to 43 
        #
        #Lets call average annual temperature 7.5C, with average summer temps of 19C
        # so the mean temp will rise from 7.5C in May to 19C in July, and back down to
        # 7.5 in October
        #
        #May starts on day 121
        date = date-121
        date_mean_temp = math.sin( (2.0*(date)*math.pi) / (365.0) ) * (19-7.5) + 7.5

        random.seed(seed_add(random_seed, 390752))
        #lets let daily actual temperatures vary around the mean by way of a normal distribution
        # where 95%-ish remain within +/- 20C from the mean (so one standard devation will be 10)

        return random.normalvariate(date_mean_temp, 10)
        
    def draw_RH(self, date, random_seed=None):
        #from the Western Regional Climate Center
        #http://www.wrcc.dri.edu/narratives/OREGON.htm
        #The afternoon average relative humidity ranges between 75 and 85 percent in January, 
        #while in July this drops to 25 or 30 percent east of the Cascades and slightly higher
        #  on the western side.  Relative humidities of 10 to 20 percent often occur under extreme
        # conditions during the summer and early fall.

        date_mean_humidity = math.cos( (2.0*(date)*math.pi) / (365.0) ) * (80-15) + 15
        
        #lets let actual humidity vary +/- 5%
        random.seed(seed_add(random_seed, 985727))
        rh = random.normalvariate(date_mean_humidity, 2.5)
        if rh < 0: rh = 0.0
        if rh > 100: rh = 100.0
        return rh

    def draw_rain(self, date, random_seed=None):
        #from http://www.na.fs.fed.us/spfo/pubs/silvics_manual/Volume_1/pinus/ponderosa.htm
        # July, August, and September are dry; average rainfall is less than 25 mm
        #
        #that's ~ 0.8 mm per day. Lets draw from an exponential with mean = 0.8
        mean_summer_precip = 0.8 #mm
        random.seed(seed_add(random_seed, 792723))
        rainfall = random.expovariate(1.0 / mean_summer_precip)

        #cutting it off, so that many values are zero
        if rainfall < 0.8: rainfall = 0.0

        return rainfall


    def get_month(self, day):
        """Return the numeral month, given the day-of-the-year"""
        if day <= 31:
            #january
            return 1
        elif day <= (31+28):
            #february
            return 2
        elif day <= (31+28+31):
            #march
            return 3
        elif day <= (31+28+31+30):
            #april
            return 4
        elif day <= (31+28+31+30+31):
            #may
            return 5
        elif day <= (31+28+31+30+31+30):
            #june
            return 6
        elif day <= (31+28+31+30+31+30+31):
            #july
            return 7
        elif day <= (31+28+31+30+31+30+31+31):
            #august
            return 8
        elif day <= (31+28+31+30+31+30+31+31+30):
            #september
            return 9
        elif day <= (31+28+31+30+31+30+31+31+30+31):
            #october
            return 10
        elif day <= (31+28+31+30+31+30+31+31+30+31+30):
            #november
            return 11
        else:
            #december
            return 12


def seed_add(seed, value):
    #if the seed is None, normally that uses system time, but I can't add values to it
    #So here, grab a system-time-seeded random val instead, and use it for the base seed
    if not seed:
        random.seed(None)
        seed = random.randint(-1000000,1000000)

    return seed + value