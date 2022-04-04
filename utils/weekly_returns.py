from cProfile import label
import pandas as pd 

import numpy as np 

import streamlit as st 

def weekly_returns(security_df):

    weekly_change = []

    for num in range(security_df.shape[0]-1):
    
        if (security_df.index[num+1] - security_df.index[num]).days > 2:
            weekly_change.append("last_day_of_week")
        
        else:
            weekly_change.append("weekday")
        
    if (security_df.index[security_df.shape[0]-1] - security_df.index[security_df.shape[0] - 2]).days > 2:
        weekly_change.append("weekday")
    
    else:
        weekly_change.append("weekday") 

    security_df["week_day_status"] = weekly_change

    weekly_close = []

    weekly_closing_price = None

    for num in range(security_df.shape[0]):
        
        if security_df["week_day_status"].values[num] == "last_day_of_week" :
            
            weekly_closing_price = np.round(security_df["Close"].values[num],3)
            
            weekly_close.append(weekly_closing_price)
            
        else: 
            
            weekly_close.append(weekly_closing_price)   

    security_df["weekly_close"] = weekly_close

    st.metric(
        label="Week to day",
        value=security_df["weekly_close"][-1],
        delta=(((security_df["Close"] - security_df["weekly_close"])/security_df["weekly_close"]) * 100)[-1]
    )

