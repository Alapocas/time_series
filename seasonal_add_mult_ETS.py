# µ¼ÈëÄ£¿é
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from math import sqrt
import pandas as pd
import numpy as np
import csv

df1 = pd.read_csv("Book1.csv")
data = pd.DataFrame(df1[["Month","average AQI value"]], columns = ["Month","average AQI value"])
data.columns = ["month", "aav"]
print(data)
#data["aav"].plot(title = "Time series")
actual = pd.DataFrame(data.iloc[12:].reset_index(drop=True))
actual.columns = ["month", "y_t"]

#initialization
#s = [-7.79, -4.19, 4.31, 1.91, 12.61, 16.01, 18.91, 24.01, -9.99, -17.82, -19.56, -18.41]
s = [0.84, 0.91, 1.22, 0.95, 1.24, 1.06, 1.05, 1.08, 0.49, 0.76, 0.93, 1.05]
l = [24.18]
b = [0.11]
alpha = 0.432
beta = 0.008
gama = 0.5772

for i in range(len(actual)-11):
    lt = alpha*(actual.ix[i, "y_t"]/s[i])+(1-alpha)*(l[i]+b[i])
    bt = beta*(lt-l[i])+(1-beta)*b[i]
    st = gama*(actual.ix[i, "y_t"]/(l[i]+b[i]))+(1-gama)*s[i]
    ft = (l[i]+b[i])*s[i]
    actual.ix[i, "l_t"] = lt
    actual.ix[i, "b_t"] = bt
    actual.ix[i, "s_t"] = st
    actual.ix[i, "f_t"] = ft
    l.append(lt)
    b.append(bt)
    s.append(st)
'''
for i in range(len(actual)-11):
    lt = alpha*(actual.ix[i, "y_t"]-s[i])+(1-alpha)*(l[i]+b[i])
    bt = beta*(lt-l[i])+(1-beta)*b[i]
    st = gama*(actual.ix[i, "y_t"]-l[i]-b[i])+(1-gama)*s[i]
    ft = l[i]+b[i]+s[i]
    actual.ix[i, "l_t"] = lt
    actual.ix[i, "b_t"] = bt
    actual.ix[i, "s_t"] = st
    actual.ix[i, "f_t"] = ft
    l.append(lt)
    b.append(bt)
    s.append(st)
'''
print(actual)
#actual[["y_t", "f_t"]].plot(title = "ETS(A, M)")
#actual[["y_t", "f_t"]].plot(title = "ETS(A, A)")
x = list(range(len(actual)-11, len(actual)+128))
y = [(l[-1]+(i+1)*b[-1])*s[-12+i] for i in range(139)]
#y = [l[-1]+(i+1)*b[-1]+s[-12+i] for i in range(139)]
plt.plot(list(range(len(actual)-11))+x, list(actual.y_t)[:228]+[None for i in range(len(y))], color = "red")
plt.plot(list(range(len(actual)-11))+x, [None for i in range(228)]+y, linestyle="--", color="green")
RMSE = 0
for i in range(11):
    actual.ix[228+i, "y_t"]
    RMSE += (actual.ix[228+i, "y_t"]-y[i])**2
RMSE = sqrt(RMSE)
print(RMSE)
