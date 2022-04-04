import datetime as dt
import time

import yfinance as yf
import pandas as pd
import numpy as np

import streamlit as st 

def days_from_ath(security_df):

    high_values = []
    for val in security_df["High"].values:
        if len(high_values) == 0:
            high_values.append(val)
        elif val > high_values[-1]:
            high_values.append(val)
        else:
            high_values.append(high_values[-1])

    security_df["All Time High"] = high_values
    security_df["CHG From All Time High"] = (security_df["Low"]/security_df["All Time High"]) - 1

    days_btwn_aths = []
    count = 0
    for num in range(security_df["All Time High"].shape[0]):
        if security_df["High"][num] == security_df["All Time High"][num] :
            count = 0
            days_btwn_aths.append(count)
            
        else:
            count += 1
            days_btwn_aths.append(count)
            
            
    security_df["Days From ATH"] = days_btwn_aths
    security_df["daily_returns"] = (security_df["Close"]/security_df["Close"].shift(1)) - 1
    col1, col2 = st.columns(2)

    if security_df.shape[0] != None:

        with col1:
            st.metric(
                label="Price change",
                value=np.round(list(security_df["Close"])[-1], 3),
                delta=str( np.round((list(security_df["daily_returns"])[-1])*100, 3)) + "%"
                )
        with col2:
            st.metric(
                label="Trading days since All Time High", 
                value=list(security_df["Days From ATH"])[-1], 
                delta=str( np.round((list(security_df["CHG From All Time High"])[-1])*100, 3)) + "%"
                )

        st.header("Trading sessions information")

        columns = ["Close","Open","High","Low","Volume"]

        st.table(security_df[columns].tail(10))





