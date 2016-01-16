"""
API Endpoints to be used in the UI.
"""

from WebSite import app, naive_bayes, k_neighbours
from flask import make_response, request

from flask_peewee.rest import RestAPI, Authentication, UserAuthentication, RestResource
from peewee import Model
from models import Card
from WebSite import app, db
from datetime import datetime
import json
import csv


@app.route('/api/bootstrap', methods=['POST', 'GET'])
def bootstrap():
    Card.delete().execute()
    
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

    decks_file = "WebSite/hearthstonedecks.csv"
    raw_data = []

    load_dataset(decks_file, raw_data)
    print("Raw_data: " + repr(len(raw_data)))
    
    #for data_dict in raw_data:
    #    Card.create(**data_dict)
    with db.database.atomic():
        step = 5000
        for idx in range(0, len(raw_data), step):
            Card.insert_many(raw_data[idx:idx + step]).execute()
            print("Inserted: " + repr(idx))
        #Card.insert_many(raw_data).execute()

    naive_bayes.process_data(raw_data)
    return make_response("Success")
    

@app.route('/api/cards/count', methods=['GET'])
def cardsCount():
    count = Card.select().count()
    return make_response(str(count))


@app.route('/api/deck/', methods=['POST'])
def analyseDeck():
    deck = request.get_json()
    pass