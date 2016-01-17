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

k_neighbours = Classifiers.KNearestDecks()
naive_bayes = Classifiers.NaiveBayes()

cards = Card.select().execute()
for card in cards:
    entry = {
        "title": card.title,
        "card_name": card.card_name,
        "card_count": card.card_count,
        "hero_class": card.hero_class,
        "archetype": card.archetype,
        "season": card.season,
        "game_mode": card.game_mode 
    }
    naive_bayes.add_card(entry)
    k_neighbours.update_deck(entry)


import WebSite.api
import WebSite.views

