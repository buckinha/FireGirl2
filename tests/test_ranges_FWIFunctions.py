import utils.FWIFunctions as FWI
import random


def test_range_FFMC():
    #testing range of outputs for FWIFunctions.FFMC()
    #signature is: FFMC(TEMP,RH,WIND,RAIN,FFMCPrev)

    max_val = float("-inf")
    min_val = float("inf")

    for i in range(5000):
        temp = random.uniform(-30,40) #degrees C
        rh = random.uniform(0,100) #%
        wind = random.uniform(0,50) #kph
        rain = random.uniform(0,500) #mm rain in 24 hours

        FFMCPrev3 = FWI.FFMC(temp,rh,wind,rain,50) #<--- final param started at zero, and then varied based on the output range
        FFMCPrev2 = FWI.FFMC(temp,rh,wind,rain,FFMCPrev3)
        FFMCPrev1 = FWI.FFMC(temp,rh,wind,rain,FFMCPrev2)
        FFMCPrev  = FWI.FFMC(temp,rh,wind,rain,FFMCPrev1)

        new_val = FWI.FFMC(temp,rh,wind,rain,FFMCPrev)
        max_val = max(new_val, max_val)
        min_val = min(new_val, min_val)

    drier_FFMC = FWI.FFMC(50, 0, 50, 0, 50)
    if drier_FFMC < 50:
        print("Higher fine fuel moisutre codes(FFMC) indicate LESS drought")
    else:
        print("Higher fine fuel moisutre codes(FFMC) indicate MORE drought")
    print("Max FFMC: {0}".format(max_val))
    print("Min FFMC: {0}".format(min_val))


def test_range_DMC():
    #testing range of outputs for FWIFunctions.DMC()
    #signature is: DMC(TEMP,RH,RAIN,DMCPrev,LAT,MONTH)
    max_val = float("-inf")
    min_val = float("inf")

    for i in range(5000):
        temp = random.uniform(-30,40) #degrees C
        rh = random.uniform(0,100) #%
        rain = random.uniform(0,500) #mm rain in 24 hours
        lat = random.uniform(-90,90)
        month = random.randint(1,12)

        DMCPrev3 = FWI.DMC(temp, rh, rain, 50      , lat, month)
        DMCPrev2 = FWI.DMC(temp, rh, rain, DMCPrev3, lat, month)
        DMCPrev1 = FWI.DMC(temp, rh, rain, DMCPrev2, lat, month)
        DMCPrev  = FWI.DMC(temp, rh, rain, DMCPrev1, lat, month)

        new_val = FWI.DMC( temp, rh, rain, DMCPrev,  lat, month)
        max_val = max(new_val, max_val) 
        min_val = min(new_val, min_val)


    drier_duff = FWI.DMC(50, 0, 0, 50    , 40, 6)
    if drier_duff < 50:
        print("Higher duff moisture codes (DMC) indicate LESS drought")
    else:
        print("Higher duff moisture codes (DMC) indicate MORE drought")
    print("Max FFMC: {0}".format(max_val))
    print("Min FFMC: {0}".format(min_val))


def test_range_DC():
    #testing output range for FWIFunctions.DC()
    #signature is DC(TEMP,RAIN,DCPrev,LAT,MONTH)

    max_val = float("-inf")
    min_val = float("inf")

    for i in range(5000):
        temp = random.uniform(-30,40) #degrees C
        rain = random.uniform(0,500) #mm rain in 24 hours
        lat = random.uniform(-90,90)
        month = random.randint(1,12)

        DCPrev3 = FWI.DC(temp, rain, 50     , lat, month)
        DCPrev2 = FWI.DC(temp, rain, DCPrev3, lat, month)
        DCPrev1 = FWI.DC(temp, rain, DCPrev2, lat, month)
        DCPrev  = FWI.DC(temp, rain, DCPrev1, lat, month)

        new_val = FWI.DC(temp, rain, DCPrev,  lat, month)
        max_val = max(new_val, max_val) 
        min_val = min(new_val, min_val)

    drier_DC = FWI.DC(50, 0, 50    , 40, 6)
    if drier_DC < 50:
        print("Higher drought codes (DC) indicate LESS drought")
    else:
        print("Higher drought codes (DC) indicate MORE drought")

    print("Max FFMC: {0}".format(max_val))
    print("Min FFMC: {0}".format(min_val))


def test_range_ISI():
    #testing output range for FWIFunctions.ISI()
    #signature is ISI(WIND,FFMC)
    max_val = float("-inf")
    min_val = float("inf")

    for i in range(5000):
        temp = random.uniform(-30,40) #degrees C
        rh = random.uniform(0,100) #%
        wind = random.uniform(0,50) #kph
        rain = random.uniform(0,500) #mm rain in 24 hours

        FFMCPrev3 = FWI.FFMC(temp,rh,wind,rain,50) #<--- final param started at zero, and then varied based on the output range
        FFMCPrev2 = FWI.FFMC(temp,rh,wind,rain,FFMCPrev3)
        FFMCPrev1 = FWI.FFMC(temp,rh,wind,rain,FFMCPrev2)
        FFMCPrev  = FWI.FFMC(temp,rh,wind,rain,FFMCPrev1)
        FFMC_val  = FWI.FFMC(temp,rh,wind,rain,FFMCPrev)

        new_val = FWI.ISI(wind, FFMC_val)

        max_val = max(new_val, max_val)
        min_val = min(new_val, min_val)

    higher_wind_ISI = FWI.ISI(20, 50)
    lower_wind_ISI = FWI.ISI(1,50)
    if higher_wind_ISI < lower_wind_ISI:
        print("Higher initial spread index (ISI) indicates SLOWER spread")
    else:
        print("Higher initial spread index (ISI) indicates FASTER spread")
    print("Max FFMC: {0}".format(max_val))
    print("Min FFMC: {0}".format(min_val))

def test_range_BUI():
    #testing the output range on FWIFunctions.BUI()
    #signature is BUI(DMC,DC)

    max_val = float("-inf")
    min_val = float("inf")

    for i in range(5000):
        temp = random.uniform(-30,40) #degrees C
        rh = random.uniform(0,100) #%
        rain = random.uniform(0,500) #mm rain in 24 hours
        lat = random.uniform(-90,90)
        month = random.randint(1,12)

        DMCPrev3 = FWI.DMC(temp, rh, rain, 50      , lat, month)
        DMCPrev2 = FWI.DMC(temp, rh, rain, DMCPrev3, lat, month)
        DMCPrev1 = FWI.DMC(temp, rh, rain, DMCPrev2, lat, month)
        DMCPrev  = FWI.DMC(temp, rh, rain, DMCPrev1, lat, month)
        DMC_val = FWI.DMC( temp, rh, rain, DMCPrev,  lat, month)

        DCPrev3 = FWI.DC(temp, rain, 50     , lat, month)
        DCPrev2 = FWI.DC(temp, rain, DCPrev3, lat, month)
        DCPrev1 = FWI.DC(temp, rain, DCPrev2, lat, month)
        DCPrev  = FWI.DC(temp, rain, DCPrev1, lat, month)
        DC_val = FWI.DC(temp, rain, DCPrev,  lat, month)

        new_val = FWI.BUI(DMC_val, DC_val)

        max_val = max(new_val, max_val) 
        min_val = min(new_val, min_val)


    more_drought_BUI = FWI.BUI(50,50)
    less_drought_BUI = FWI.BUI(1,1)
    if less_drought_BUI < more_drought_BUI:
        print("Higher build-up index (BUI) indicate MORE drought")
    else:
        print("Higher build-up index (BUI) indicate LESS drought")

    print("Max FFMC: {0}".format(max_val))
    print("Min FFMC: {0}".format(min_val))

def test_range_FWI():
    #testing the output range of FWIFunctions.FWI()
    #signature is FWI(ISI, BUI)

    max_val = float("-inf")
    min_val = float("inf")

    for i in range(5000):
        temp = random.uniform(-30,40) #degrees C
        rh = random.uniform(0,100) #%
        rain = random.uniform(0,500) #mm rain in 24 hours
        wind = random.uniform(0,50) #kph
        lat = random.uniform(-90,90)
        month = random.randint(1,12)

        DMCPrev3 = FWI.DMC(temp, rh, rain, 50      , lat, month)
        DMCPrev2 = FWI.DMC(temp, rh, rain, DMCPrev3, lat, month)
        DMCPrev1 = FWI.DMC(temp, rh, rain, DMCPrev2, lat, month)
        DMCPrev  = FWI.DMC(temp, rh, rain, DMCPrev1, lat, month)
        DMC_val = FWI.DMC( temp, rh, rain, DMCPrev,  lat, month)

        DCPrev3 = FWI.DC(temp, rain, 50     , lat, month)
        DCPrev2 = FWI.DC(temp, rain, DCPrev3, lat, month)
        DCPrev1 = FWI.DC(temp, rain, DCPrev2, lat, month)
        DCPrev  = FWI.DC(temp, rain, DCPrev1, lat, month)
        DC_val = FWI.DC(temp, rain, DCPrev,  lat, month)

        BUI_val = FWI.BUI(DMC_val, DC_val)

        FFMCPrev3 = FWI.FFMC(temp,rh,wind,rain,50) 
        FFMCPrev2 = FWI.FFMC(temp,rh,wind,rain,FFMCPrev3)
        FFMCPrev1 = FWI.FFMC(temp,rh,wind,rain,FFMCPrev2)
        FFMCPrev  = FWI.FFMC(temp,rh,wind,rain,FFMCPrev1)
        FFMC_val  = FWI.FFMC(temp,rh,wind,rain,FFMCPrev)

        ISI_val = FWI.ISI(wind, FFMC_val)

        new_val = FWI.FWI(ISI_val, BUI_val)

        max_val = max(new_val, max_val) 
        min_val = min(new_val, min_val)


    higher_wind_FWI = FWI.FWI(20, 50)
    lower_wind_FWI = FWI.FWI(1,50)
    if higher_wind_FWI < lower_wind_FWI:
        print("Higher fire weather index (FWI) indicates SLOWER spread")
    else:
        print("Higher fire weather index (FWI) indicates FASTER spread")

    print("Max FFMC: {0}".format(max_val))
    print("Min FFMC: {0}".format(min_val))


def test_ranges_all():
    test_range_FFMC()
    print("")
    test_range_DMC()
    print("")
    test_range_DC()
    print("")
    test_range_ISI()
    print("")
    test_range_BUI()
    print("")
    test_range_FWI()
    print("")


if __name__ == "__main__":
    print("Testing Ranges for FWIFunctions")
    print("")
    test_ranges_all()