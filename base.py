from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import datetime as dt
import time

import yfinance as yf
import pandas as pd
import numpy as np

from utils import moving_averages

app = Flask(__name__)

app.config["SECRET_KEY"] = "MYSECRETKEY"

def fetch_data(ticker):
    security_df = yf.Ticker(ticker).history(start="2010-01-01", end="2023-01-01")
    return security_df

def daily_returns(df):
    df["daily_returns"] = ((df["Close"]/df["Close"].shift(1)) - 1)*100
    return df

class InfoForm(FlaskForm):

    ticker = StringField("Enter the ticker symbol", validators=[DataRequired()])
    submit = SubmitField("submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session["ticker"] = form.ticker.data

        security_df = fetch_data(session["ticker"])

        security_df = moving_averages.moving_avg(security_df, 200)

        security_df = moving_averages.moving_avg(security_df, 100)

        security_df = moving_averages.moving_avg(security_df, 50)

        security_df = moving_averages.moving_avg(security_df, 30)

        security_df = moving_averages.moving_avg(security_df, 20)

        security_df = moving_averages.moving_avg(security_df, 14)

        security_df = moving_averages.moving_avg(security_df, 7)

        temp_df = security_df.tail(20)

        session['Date'] = list(temp_df.index.astype(str))

        session['Close'] = list(moving_averages.rounding(temp_df["Close"]))

        session["200DMA"] = list(moving_averages.rounding(temp_df["200DMA"]))

        session["100DMA"] = list(moving_averages.rounding(temp_df["100DMA"]))

        session["50DMA"] = list(moving_averages.rounding(temp_df["50DMA"]))

        session["30DMA"] = list(moving_averages.rounding(temp_df["30DMA"]))

        session["20DMA"] = list(moving_averages.rounding(temp_df["20DMA"]))

        session["14DMA"] = list(moving_averages.rounding(temp_df["14DMA"]))

        session["7DMA"] = list(moving_averages.rounding(temp_df["7DMA"]))

        session["200DMA CHG"] = list(moving_averages.rounding(temp_df["200DMA CHG"] * 100))

        session["100DMA CHG"] = list(moving_averages.rounding(temp_df["100DMA CHG"] * 100))

        session["50DMA CHG"] = list(moving_averages.rounding(temp_df["50DMA CHG"] * 100))

        session["30DMA CHG"] = list(moving_averages.rounding(temp_df["30DMA CHG"] * 100))

        session["20DMA CHG"] = list(moving_averages.rounding(temp_df["20DMA CHG"] * 100))

        session["14DMA CHG"] = list(moving_averages.rounding(temp_df["14DMA CHG"] * 100))

        session["7DMA CHG"] = list(moving_averages.rounding(temp_df["7DMA CHG"] * 100))

        session["Close"] = list(moving_averages.rounding(temp_df["Close"]))

        session["% Change"] = list(moving_averages.rounding(daily_returns(temp_df)["daily_returns"]))

        session['temp'] = list(
            zip(
                session["Date"],
                session["Close"],
                session["200DMA"],
                session["100DMA"],
                session["50DMA"],
                session["30DMA"],
                session["20DMA"],
                session["14DMA"],
                session["7DMA"],
                session["200DMA CHG"],
                session["100DMA CHG"],
                session["50DMA CHG"],
                session["30DMA CHG"],
                session["20DMA CHG"],
                session["14DMA CHG"],
                session["7DMA CHG"]
                )
            )

        return redirect(url_for("MovAvg"))
    
    return render_template("base.html",form=form)

@app.route('/MovAvg')
def MovAvg():
    return render_template("MovAvg.html")

if __name__ == '__main__':
    app.run(debug=True)