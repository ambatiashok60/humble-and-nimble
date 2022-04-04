import pandas as pd 
import numpy as np 
import streamlit as st 
import plotly.express as ex
import plotly.graph_objects as go


def plot_bollinger_bands(df):
    
    fig = go.Figure()

    check =  all(item in df.columns for item in ["middle_band", "upper_band", "lower_band"])

    if check is False:
        df["middle_band"] = df["Close"].rolling(window=20).mean()
        df["upper_band"] = df["middle_band"] + (2 * df["Close"].rolling(window=20).std())
        df["lower_band"] = df["middle_band"] - (2 * df["Close"].rolling(window=20).std())

    if df.shape[0] > 200:
    
        upper_band_plot = go.Scatter(x=df.index[-200:], y=df["upper_band"][-200:],line=dict(color='#B33030', width=2), 
                                    name="upper band")
        
        middle_band_plot = go.Scatter(x=df.index[-200:], y=df["middle_band"][-200:],line=dict(color='#F6FFA4', width=1.5), 
                                    name="middle bandt")
        
        lower_band_plot = go.Scatter(x=df.index[-200:], y=df["lower_band"][-200:],line=dict(color='#06FF00', width=2), 
                                    name="lower band")
    else:

        upper_band_plot = go.Scatter(x=df.index, y=df["upper_band"],line=dict(color='#B33030', width=2), 
                                    name="upper band")
        
        middle_band_plot = go.Scatter(x=df.index, y=df["middle_band"],line=dict(color='#F6FFA4', width=1.5), 
                                    name="middle band")
        
        lower_band_plot = go.Scatter(x=df.index, y=df["lower_band"],line=dict(color='#06FF00', width=2), 
                                    name="lower band")

    fig.add_trace(upper_band_plot)
    fig.add_trace(middle_band_plot)
    fig.add_trace(lower_band_plot)
    
    fig.update_xaxes(title="Date", rangeslider_visible=True)
    fig.update_yaxes(title="Price", autorange=True, fixedrange=False)
    fig.update_layout(showlegend=True)

    st.info("bollinger band window size is 20")

    col1, col2, col3 = st.columns(3)

    def rounding(data, rounding_decimals = 3):
        return np.round(data, rounding_decimals)

    col1.metric(
        label="upper band",
        value= rounding(df["upper_band"][-1]),
        delta= rounding(((df["Close"][-1] - df["upper_band"][-1])/df["upper_band"][-1])*100)
    )
    col2.metric(
        label="middle band",
        value= rounding(df["middle_band"][-1]),
        delta= rounding(((df["Close"][-1] - df["middle_band"][-1])/df["middle_band"][-1])*100)
    )
    col3.metric(
        label="lower band",
        value= rounding(df["lower_band"][-1]),
        delta= rounding(((df["Close"][-1] - df["lower_band"][-1])/df["lower_band"][-1])*100)
    )
    
    st.plotly_chart(fig)
    