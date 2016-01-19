"""
API Endpoints to be used in the UI.
"""

from WebSite import app, naive_bayes, k_neighbours
from flask import make_response, request, current_app
from flask.ext.cors import CORS, cross_origin
from functools import update_wrapper

from models import Card
from WebSite import app, db
from datetime import datetime, timedelta
from heapq import heappush

import json
import csv

CORS(app)

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
    
    with db.database.atomic():
        step = 100
        for idx in range(0, len(raw_data), step):
            Card.insert_many(raw_data[idx:idx + step]).execute()
            print("Inserted: " + repr(idx))

    cards = Card.select().execute()
    for card in raw_data:
        naive_bayes.add_card(card)
        k_neighbours.update_deck(card)
    return make_response("Success")
    

@app.route('/api/cards/count', methods=['GET'])
def cards_count():
    count = Card.select().count()
    return make_response(str(count))


@app.route('/api/deck/classify', methods=['POST'])
def deck_classify():
    data = request.get_json()
    hero_class = data["hero_class"]
    deck = data["deck"]
    K = 3
    if "nearest" in data:
        try:
            K = int(data["nearest"])
        except ValueError:
            K = 3

    archetypes = naive_bayes.classify(hero_class, deck)
    print(repr(archetypes))
    sorted_archetypes = []
    for key in archetypes:
        heappush(sorted_archetypes, ( 0 - archetypes[key], key))

    treshold, sum = 0.5, 0
    top_archetypes = []
    for prob, archetype in sorted_archetypes:
        if sum < treshold:
            sum+= (0-prob)
            top_archetypes.append(archetype)
            
    nearest = k_neighbours.get_nearest_decks(K, hero_class, top_archetypes, deck)

    has_match = False
    for dist, near_entry in nearest:
        has_match |= near_entry['complete_match']
        if near_entry['complete_match'] and number_of_cards(near_entry["deck"]) < number_of_cards(deck):
            update_old_deck(near_entry["deck"], deck)

    if not has_match and number_of_cards(deck) > 10:
        inser_new_deck(hero_class, top_archetypes[0], deck)
        pass

    return make_response(json.dumps({
        "archetypes": archetypes,
        "nearest": nearest,
        "has_match": has_match
        }))

def number_of_cards(deck):
    """The number of cards in a deck."""
    count = 0
    for card in deck:
        print(repr(card))
        card_count = int(card['card_count'])
        count += card_count
    return count

def update_old_deck(old_deck, new_deck):
    """When the old deck has fewer cards that the new one, inserts the missing entries"""
    for new_card in new_deck:
        found = False
        for old_card in old_deck:
            if new_card['card_name'] == old_card['card_name']:
                found = True
                if new_card['card_count'] > old_card['card_count']:
                    add_card_entry(old_card)
        if not found:
            new_card["title"] = old_card["title"]
            new_card["hero_class"] = old_card["hero_class"]
            new_card["archetype"] = old_card["archetype"]
            add_card_entry(card)


def inser_new_deck(hero_class, archetype, deck):
    """Inserts a new deck card by card"""
    title = "Deck from " + datetime.now().isoformat()
    for card in deck:
        card["title"] = title
        card["hero_class"] = hero_class
        card["archetype"] = archetype
        add_card_entry(card)

def add_card_entry(card):
    #card["card_count"] = int(card["card_count"])
    naive_bayes.add_card(card)
    k_neighbours.update_deck(card)
    Card.insert_many([card]).execute()