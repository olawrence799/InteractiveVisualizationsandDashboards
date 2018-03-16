# import necessary libraries
from sqlalchemy import func

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import create_engine, MetaData
import os
from sqlalchemy.orm import Session

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)

Base = automap_base()
dbfile = os.path.join('db', 'belly_button_biodiversity.sqlite')
engine = create_engine(f"sqlite:///{dbfile}")
# engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")
Base.prepare(engine, reflect=True)
Osample = Base.classes.samples  
session = Session(engine)
# conn = engine.connect()

class Name(db.Model):
    __tablename__ = 'samples_metadata'

    id = db.Column(db.Integer, primary_key=True)
    AGE = db.Column(db.Integer)
    BBTYPE = db.Column(db.Text)
    ETHNICITY = db.Column(db.Text)
    GENDER = db.Column(db.Text)
    LOCATION = db.Column(db.Text)
    SAMPLEID = db.Column(db.Integer)
    WFREQ = db.Column(db.Integer)

class Otu(db.Model):
    __tablename__ = 'otu'

    id = db.Column(db.Integer, primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.Text)


# Create database classes
@app.before_first_request
def setup():
    # Recreate database each time for demo
    #db.drop_all()
    db.create_all()


#################################################
# Flask Routes
#################################################


# Query the database and send the jsonified results
@app.route("/names")
def names():
    sel = [
        func.distinct(Name.SAMPLEID)
    ]
    results = db.session.query(*sel)

    names = [row[0] for row in results]
    for i in range(0,len(names)):
        names[i] = "BB_" + str(names[i])
        i = i + 1
    return jsonify(names)

@app.route("/otu")
def otus():
    sel = [
        Otu.lowest_taxonomic_unit_found
    ]
    results = db.session.query(*sel)

    otus = [row[0] for row in results]
    return jsonify(otus)

@app.route("/metadata/<sample>")
def sample(sample):
    sample_trim = sample[3:]
    results = db.session.query(Name.AGE, Name.BBTYPE, Name.ETHNICITY, Name.GENDER, Name.LOCATION, Name.SAMPLEID).filter(Name.SAMPLEID==(sample_trim)).all()
    age = [row[0] for row in results][0]
    bbtype = [row[1] for row in results][0]
    ethnicity = [row[2] for row in results][0]
    gender = [row[3] for row in results][0]
    location = [row[4] for row in results][0]
    sampleid = [row[5] for row in results][0]
    return jsonify({'AGE': age, 'BBTYPE': bbtype, 'ETHNICITY': ethnicity, 'GENDER': gender, 'LOCATION': location, 'SAMPLEID': sampleid})

@app.route("/wfreq/<sample>")
def wsample(sample):
    sample_trim = sample[3:]
    results = db.session.query(Name.WFREQ).filter(Name.SAMPLEID==(sample_trim))
    wfreq = [row[0] for row in results]
    return jsonify(wfreq)

@app.route("/samples/<sample>")
def osample(sample):
    col_name = sample
    results = session.query(Osample.otu_id, getattr(Osample, col_name)).filter(getattr(Osample, col_name) > 0).\
        order_by(getattr(Osample, col_name).desc()).all()

    otu_ids = [row[0] for row in results]
    sample_values = [row[1] for row in results]

    return jsonify([{'otu_ids': otu_ids, 'sample_values': sample_values}])

# create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)