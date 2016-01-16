"""
The flask application package.
"""

from flask import Flask
from flask_peewee.db import Database

import Classifiers


app = Flask(__name__)
app.config.from_object('WebSite.config')


# instantiate the db wrapper
db = Database(app)

from models import Card

if Card.table_exists() == False:
    Card.create_table()

k_neighbours = Classifiers.KNearestNeighbours()
naive_bayes = Classifiers.NaiveBayes()

cards = Card.select().execute()
naive_bayes.process_data(cards)


import WebSite.api
import WebSite.views

