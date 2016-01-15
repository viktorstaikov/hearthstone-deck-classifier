# models
from peewee import *
from datetime import datetime
import json
from FlaskWebProject1 import db


class Card(db.Model):
    
    # custom fields
    title = CharField(unique=True, null=False)
    card_name = CharField(unique=True, null=False)
    card_count = IntegerField()
    hero_class = CharField(unique=True, null=False)
    archetype = CharField(unique=True, null=False)
    season = CharField(unique=True, null=False)
    game_mode = CharField(unique=True, null=False)

    def to_JSON(self):
        d = self.__dict__['_data']
        return json.dumps(d)