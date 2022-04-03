from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = "MYSECRETKEY"

class InfoForm(FlaskForm):

    ticker = StringField("Enter the ticker symbol", validators=[DataRequired()])
    submit = SubmitField("submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session["ticker"] = form.ticker.data
        return redirect(url_for("insights"))
    
    return render_template("base.html",form=form)

@app.route('/insights')
def insights():
    return render_template("insights.html")

if __name__ == '__main__':
    app.run(debug=True)