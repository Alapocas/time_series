import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def exp_smoothing(ts,extra_periods=1, alpha=0.2, plot=False):
     
    """
    This function calculates a forecast with an exponential smoothing method.
     
    Inputs
      - ts: the historical values (a list, a numpy array or a pandas series)
      - extra_perios: the number of data points that you want to forecast
      - alpha: the alpha parameter
      - plot: if True the function will print the dataset and a plot of the forecast
    """
     
    #
    # - Clean input 
    #
     
    # Avoid any edition of original list, array or dataframe
    ts = ts.copy()
    # Transform ts into list if needed
    
    try:
        ts = ts.tolist()
    except:
        pass
    
    #
    # - Forecast Creation
    #
     
    # Define forecast
    f = [np.nan]
     
    # Initialize first point of forecast
    f.append(ts[0])
     
    # Create all the m+1 forecast
    for t in range(1,len(ts)-1):
        f.append((1-alpha)*f[-1]+alpha*ts[t])
         
    # Forecast for all extra months
    for t in range(extra_periods):
        # Update the forecast as the last forecast
        f.append(f[-1])    
        # fill in ts by np.nan for easy plotting and dataframe creation if any
        ts.append(np.nan)
 
    #
    # - Analysis &amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp; results
    #
     
    # Populate table with all the results    
    dic = {"demand":ts,"forecast":f}
    results = pd.DataFrame.from_dict(dic)
    results.index.name = 'Period'
    results["error"] = results["demand"] - results["forecast"]
     
    # Computes the Mean Absolute Error Percentage
    if results["demand"].sum():
        maep = abs(results["error"]).sum()/(results["demand"].sum()) 
    else:
        maep = 1
 
    # Show the results if plot==True
    if plot:         
        print(results)
        print("MAE percentage:",int(maep*100),"%")  
        results[["demand","forecast"]].plot(title="Exponential Smoothing with alpha = "+str(alpha),figsize=(10,10))
        plt.ylabel("y label")
        #plt.show()
        #plot_forecast(results)
     
    # Return the full data set and an indicator of past MAEP    
    return results,maep

df1 = pd.read_csv("Book1.csv")
data = pd.DataFrame(df1[["Month","average AQI value"]], columns = ["Month","average AQI value"])
data.columns = ["month", "aav"]
ts = data["aav"]
results, maep = exp_smoothing(ts,100,0.1,True)