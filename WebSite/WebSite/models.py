# models
from peewee import *
from datetime import datetime
import json
from WebSite import db


class Card(db.Model):
    
    # custom fields
    title = CharField(null=False)
    card_name = CharField(null=False)
    card_count = IntegerField()
    hero_class = CharField(null=False)
    archetype = CharField(null=False)
    season = CharField(null=False)
    game_mode = CharField(null=False)

    def to_JSON(self):
        d = self.__dict__['_data']
        return json.dumps(d)

