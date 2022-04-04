import pandas as pd 
import numpy as np 

def moving_avg(df, days):
    temp = str(days) + "DMA"
    df[temp] = df["Close"].rolling(days).mean()
    chg_mv_avg = str(days) + "DMA CHG"
    df[chg_mv_avg] = (df["Close"] - df[temp])/df[temp]
    return df

def rounding(data, rounding_decimals = 3):
    return np.round(data, rounding_decimals)
