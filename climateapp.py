# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

#import Flask
from flask import Flask, jsonify

# Datebase
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    """Return the Climate data as json"""
    return(
        f"Welcome to the climate app homepage!<br/>"
        f"Availible routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")
    # print("Currently viewing the homepage.")

# Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipiation():
    session = Session(engine)
    """Return a list of all Precipitation Data"""
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>= "2016-08-24").all()
    session.close()

    precip = []
    for each in results:
        precip_dict = {}
        precip_dict[each[0]] = each[1]
        precip.append(precip_dict)
    # Return the JSON representation of your dictionary.
    return jsonify(precip)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Returning all stations"""
    results = session.query(Station.station).\
        order_by(Station.station).all()

    session.close()
    # converting into a list: 
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

# Query the dates and temperature observations of 
# the most active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active = session.query(Measurement.date, Measurement.tobs, Measurement.prcp)\
        .filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).all()

    session.close()
    # Converting into a dictionary
    all_tobs = []
    for prcp, date,tobs in most_active:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(all_tobs)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
         func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        
    session.close()

    start_tobs = []
    for min, avg, max in start_date:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_tobs.append(start_date_tobs_dict) 

    return jsonify(start_date)


@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    session = Session(engine)

    start_and_end_dates = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    start_and_end_tobs = []
    for min, avg, max in start_and_end_dates:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_and_end_tobs.append(start_end_tobs_dict) 
    
    return jsonify(start_and_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)