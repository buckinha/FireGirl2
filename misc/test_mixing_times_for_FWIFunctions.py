import utils.FWIFunctions as FWI
import random


def mixing_time_FFMC():

    FFMC_high = 100
    FFMC_low = 0.0001
    step_sum = 0.0
    max_steps = -1
    min_steps = 100

    sample_count = 500
    
    for i in range(sample_count):

        for j in range(100):
            temp = random.uniform(-30,40) #degrees C
            rh = random.uniform(0,100) #%
            wind = random.uniform(0,50) #kph
            rain = random.uniform(0,500) #mm rain in 24 hours

            FFMC_high = FWI.FFMC(temp, rh, wind, rain, FFMC_high)
            FFMC_low  = FWI.FFMC(temp, rh, wind, rain, FFMC_low)

            if abs(FFMC_high - FFMC_low) < 0.5:
                #print("FFMC Extreme mixing time: {0} steps".format(i))
                step_sum += j
                min_steps = min(j,min_steps)
                max_steps = max(j,max_steps)
                break

    step_ave = step_sum / float(sample_count)
    print("average mixing time for FFMC: {0} steps".format(step_ave))
    print("max convergence steps: {0}".format(max_steps))


    #print("FFMC_high: " + str(FFMC_high))
    #print("FFMC_low: " + str(FFMC_low))
    
def mixing_time_DMC():
    #DMC signature: DMC(TEMP,RH,RAIN,DMCPrev,LAT,MONTH)
    DMC_high = 100
    DMC_low = 0.0001
    step_sum = 0.0
    max_steps = -1
    min_steps = 100

    sample_count = 500

    for i in range(sample_count):

        for j in range(100):
            temp = random.uniform(-30,40) #degrees C
            rh = random.uniform(0,100) #%
            rain = random.uniform(0,500) #mm rain in 24 hours
            lat = random.uniform(-90,90)
            month = random.randint(1,12)

            DMC_high = FWI.DMC(temp, rh, rain, DMC_high, lat, month)
            DMC_low  = FWI.DMC(temp, rh, rain, DMC_low,  lat, month)

            if abs(DMC_high - DMC_low) < 0.5:
                #print("FFMC Extreme mixing time: {0} steps".format(i))
                step_sum += j
                min_steps = min(j,min_steps)
                max_steps = max(j,max_steps)
                break

    step_ave = step_sum / float(sample_count)
    print("average mixing time for DMC: {0} steps".format(step_ave))
    print("max convergence steps: {0}".format(max_steps))

def mixing_time_DC():
    #DC signature:   DC(TEMP,RAIN,DCPrev,LAT,MONTH)
    DC_high = 100
    DC_low = 0.0001
    step_sum = 0.0
    max_steps = -1
    min_steps = 100

    sample_count = 500

    for i in range(sample_count):

        for j in range(100):
            temp = random.uniform(-30,40) #degrees C
            rain = random.uniform(0,500) #mm rain in 24 hours
            lat = random.uniform(-90,90)
            month = random.randint(1,12)

            DC_high = FWI.DC(temp, rain, DC_high, lat, month)
            DC_low  = FWI.DC(temp, rain, DC_low, lat, month)

            if abs(DC_high - DC_low) < 0.5:
                #print("FFMC Extreme mixing time: {0} steps".format(i))
                step_sum += j
                min_steps = min(j,min_steps)
                max_steps = max(j,max_steps)
                break

    step_ave = step_sum / float(sample_count)
    print("average mixing time for DC: {0} steps".format(step_ave))
    print("max convergence steps: {0}".format(max_steps))


def mixing_times():
    mixing_time_FFMC()
    print("")
    mixing_time_DMC()
    print("")
    mixing_time_DC()
    print("")