# Import Dependenices 
from flask import Flask, jsonify
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd

#Create engine
engine = create_engine("sqlite:///Ref/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create an app
app = Flask(__name__)

# home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/ + start date<br>"
        f"/api/v1.0/ + start date/ + end date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    last_date = session.query(func.max(Measurement.date)).all()
    last_date = last_date[0][0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
    year_before_date = ((last_date - relativedelta(years = 1)).strftime('%Y-%m-%d'))
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before_date).order_by(Measurement.date.desc()).all()
    data = {date: prcp for date, prcp in query}
    return jsonify(data)



@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    query = session.query(Station.station).all()
    stations = list(np.ravel(query))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    last_date = session.query(func.max(Measurement.date)).all()
    last_date = last_date[0][0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
    year_before_date = ((last_date - relativedelta(years = 1)).strftime('%Y-%m-%d'))
    query = session.query(Measurement.tobs).filter(Measurement.date >= year_before_date).order_by(Measurement.date.desc()).all()
    data = list(np.ravel(query))
    return jsonify(data)

@app.route("/api/v1.0/<start>")
def startDate(start):
    print("Server received request for 'start' page...")
    query = session.query(Measurement.tobs).filter(Measurement.date >= start).all()
    df = pd.DataFrame(query)
    tmin = df.min()
    tavg = df.mean()
    tmax = df.max()
    data = [tmin, tavg, tmax]
    data = list(np.ravel(data))
    return jsonify(data)


@app.route("/api/v1.0/<start>/<end>")
def startANDendDate(start, end):
    print("Server received request for 'start/end' page...")
    query = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    df = pd.DataFrame(query) 
    tmin = df.min()
    tavg = df.mean()
    tmax = df.max()
    data = [tmin, tavg, tmax]
    data = list(np.ravel(data))
    return jsonify(data)

if __name__ == "_main_":
    app.run(debug=True)