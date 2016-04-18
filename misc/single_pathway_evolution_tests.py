import firegirl2.FGPathway
import matplotlib.pyplot as plt
import numpy as np


def stand_ages(years=100, random_seed=None):
    pw = firegirl2.FGPathway.FGPathway(random_seed=random_seed)

    age_class_percentiles = []

    for y in range(years):
        pw.simulate(1)
        age_class_percentiles.append(pw.get_age_class_percentiles())

    #build fan chart data
    age_class_perc = np.transpose(age_class_percentiles)

    x_values = range(0,years)

    plt.figure()

    #0%-100%
    plt.fill_between(x=x_values, y1=age_class_perc[0], y2=age_class_perc[10], alpha=0.1)

    #10%-90%
    plt.fill_between(x=x_values, y1=age_class_perc[1], y2=age_class_perc[9], alpha=0.1)

    #20%-80%
    plt.fill_between(x=x_values, y1=age_class_perc[2], y2=age_class_perc[8], alpha=0.1)

    #30%-70%
    plt.fill_between(x=x_values, y1=age_class_perc[3], y2=age_class_perc[7], alpha=0.1)

    #40%-60%
    plt.fill_between(x=x_values, y1=age_class_perc[4], y2=age_class_perc[6], alpha=0.1)

    #50% line
    plt.plot(x=x_values, y=age_class_perc[5])

    plt.title("Stand Age Percentiles Over Time - Single Pathway")
    plt.xlabel("Year")
    plt.ylabel("Stand Age")

    plt.show()

def fire_sizes(years=100, random_seed=None):
    pw = firegirl2.FGPathway.FGPathway(random_seed=random_seed)

    fire_sizes = []

    pw.simulate(years)

    acres_burned = [None] * years
    acres_crowned = [None] * years

    for y in range(years):
        _burned, _crowned = pw.get_fire_stats(y)
        acres_burned[y] = _burned
        acres_crowned[y] = _crowned

    plt.figure()
    x_vals = range(0,years)
    plt.plot(x_vals,acres_burned,label="Acres Burned")
    plt.plot(x_vals,acres_crowned,label="Acres Crowned")
    plt.title("Acres burned, and consumed in crown fire, per year. Single Pathway")
    plt.xlabel("Year")
    plt.ylabel("Acres Affected")
    plt.show()
        