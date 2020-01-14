import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def exp_smoothing(data, extra_periods=3, alpha=0.2, beta=0.3, plot = True):
    data = data.copy()
    level = [8]
    slope = [1]
    forecast = [np.nan]
    for i in range(1, len(data)):
        forecast.append(level[-1]+slope[-1])
        level.append(alpha*data[i]+(1-alpha)*(level[-1]+slope[-1]))
        slope.append(beta*(level[-1]-level[-2])+(1-beta)*slope[-1])
    last_l = forecast[len(data)-1]
    last_s = slope[-1]
    for i in range(extra_periods):
        forecast.append(last_l+(i+1)*last_s)
        data.append(np.nan)
        level.append(np.nan)
        slope.append(np.nan)
    dic = {"demand":data, "level":level, "slope":slope, "forecast":forecast}
    results = pd.DataFrame.from_dict(dic)
    results.index.name = "Period"
    results["error"] = results["demand"]-results["forecast"]
    if results["demand"].sum():
        maep = abs(results["error"].sum())/results["demand"].sum()
    else:
        maep = 1
    if plot:
        print(results)
        print("MAE percentage: ",maep*100,"%")
        results[["demand","forecast"]].plot(title="Trend Method",figsize=(10,10))
        plt.ylabel("number")

data = [11,9,12,13,10,14,18,16,19,20]
exp_smoothing(data)
