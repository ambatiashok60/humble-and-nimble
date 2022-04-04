import datetime as dt
import time, os

import yfinance as yf
import pandas as pd
import numpy as np

import streamlit as st 
from streamlit_option_menu import option_menu

import moving_averages , change_frm_ath, weekly_returns, bollinger_bands

dir_name = os.path.abspath(os.path.dirname(__file__))

location = os.path.join(dir_name, 'styles.css')

with open(location) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("HUMBLE AND NIMBLE")

with st.sidebar:
    selected = option_menu("Techinicals", ["Home","Moving Averages","Returns","Bollinger Bands"])

ticker = st.text_input(label="Enter ticker symbol")

# global security_df

# if st.button('ENTER'):

#     security_df = yf.Ticker(ticker).history(start="2010-01-01", end="2023-01-01")

security_df = yf.Ticker(ticker).history(start="2010-01-01", end="2023-01-01")

print(security_df.shape)

if ticker:

    if security_df.shape[0] > 0 :

        if selected == "Moving Averages":
            moving_averages.show_moving_avgs(security_df)

        if selected == "Home":
            change_frm_ath.days_from_ath(security_df)

        if selected == "Returns":
            weekly_returns.weekly_returns(security_df)

        if selected == "Bollinger Bands":
            bollinger_bands.plot_bollinger_bands(security_df)

    else:
        st.warning("Ticker doesn't exist")
