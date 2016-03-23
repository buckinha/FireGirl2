#FireGirl2/graphing/graph_growth_models.py

import matplotlib.pyplot as plt
import firegirl2.FGGrowth

def PIPO_growth_model():
    growth_model = firegirl2.FGGrowth.GrowthModel()

    #levels = range(0,20000,1000)
    levels = [0, 250, 500, 750, 1000,2000,4000,6000,8000,10000,12000,14000,16000,18000,20000]

    plt.figure()
    CP = plt.contour(growth_model.PIPO_volumes, 20, levels=levels)
    plt.clabel(CP, inline=1, fontsize=10, fmt="%1.0f")
    plt.xlabel("stand age")
    plt.ylabel("site index (m)")
    plt.title("PIPO Volume Growth Model")
    #plt.legend()
    plt.show()


if __name__ == "__main__":
    PIPO_growth_model()