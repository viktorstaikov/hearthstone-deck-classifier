"""
API Endpoints to be used in the UI.
"""

from WebSite import app, naive_bayes, k_neighbours
from flask import make_response, request

from flask_peewee.rest import RestAPI, Authentication, UserAuthentication, RestResource
from models import Card
from WebSite import app, db
from datetime import datetime
import json



@app.route('/api/bootstrap/', methods=['POST'])
def bootstrap():
    Card.delete()
    
    def load_dataset(filename, data=[], keys=[]):
        with open(filename, 'rb') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            keys = dataset[0]
            for x in range(1, len(dataset)):
                element = {}
                for y in range(len(dataset[x])):
                    element[keys[y]] = dataset[x][y]
                data.append(element)

    decks_file = "hearthstonedecks.csv"
    raw_data = []

    load_dataset(decks_file, raw_data)
    naive_bayes.process_data(raw_data)
    

@app.route('/api/deck/', methods=['POST'])
def analyseDeck():
    deck = request.get_json()
    pass