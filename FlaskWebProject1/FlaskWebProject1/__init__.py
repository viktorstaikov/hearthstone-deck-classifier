"""
The flask application package.
"""

from flask import Flask
from flask_peewee.db import Database

import Classifiers


app = Flask(__name__)
app.config.from_object('FlaskWebProject1.config')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


# instantiate the db wrapper
db = Database(app)

from models import Card

if Card.table_exists() == False:
    Card.create_table()

k_neighbours = Classifiers.KNearestNeighbours()
naive_bayes = Classifiers.NaiveBayes()



import FlaskWebProject1.api
import FlaskWebProject1.views

