# Import the dependencies.
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
connection = engine.connect()
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    connection = engine.connect()

    prcp_sql = connection.execute("SELECT measurement.date, measurement.prcp FROM measurement WHERE date BETWEEN '2016-08-23' and '2017-08-23'")
    new_df = pd.DataFrame(prcp_sql)
    df_dict = new_df.to_dict(orient = 'dict')

    return jsonify(df_dict)

@app.route("/api/v1.0/stations")
def stations():
    
    connection = engine.connect()

    stations_q = connection.execute("SELECT measurement.station FROM measurement")
    stations_df = pd.DataFrame(stations_q)
    stations_dict = stations_df.to_dict(orient = 'dict')
    
    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def stations():
    
    connection = engine.connect()

    yr_active = connection.execute("SELECT tobs FROM measurement WHERE station = 'USC00519281'AND date BETWEEN '2016-08-23' and '2017-08-23'")
    yr_df = pd.DataFrame(yr_active.all())
    active_dict = yr_df.to_dict(orient = 'dict')
    
    return jsonify(active_dict)


@app.route("/api/v1.0/tobs")
def stations():
    
    connection = engine.connect()

    yr_active = connection.execute("SELECT tobs FROM measurement WHERE station = 'USC00519281'AND date BETWEEN '2016-08-23' and '2017-08-23'")
    yr_df = pd.DataFrame(yr_active.all())
    active_dict = yr_df.to_dict(orient = 'dict')
    
    return jsonify(active_dict)


if __name__ == '__main__':
    app.run(debug=True)
