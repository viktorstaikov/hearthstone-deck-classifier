﻿class NaiveBayes(object):
    """Naive Bayes Classifier for the purpose of classifying Hearthstone Decks"""

    def __init__(self):
        self.total_cards = 0
        self.raw_data = []
        self.cards = {}
        self.all_cards = {}
        self.classes = []
        self.archetypes = []

    def __calculate_probability(self, hero_class, archetype, deck):

        if not archetype in self.cards[hero_class]:
            return 0


        # the number of cards is proportional on the number of decks
        probability = 1.0
        probability *= self.cards[hero_class][archetype]["total"] / self.cards[hero_class]["total"]
        cards_into_account = 0.0
        total_cards = 0.0
        for card in deck:
            card_name = card['card_name']
            card_count = int(card['card_count'])

            total_cards += 1

            if card_name in self.cards[hero_class][archetype]:
                # numerator 
                card_type_prob = self.cards[hero_class][archetype][card_name] / self.cards[hero_class][archetype]["total"]
                # denominator
                card_prob = self.all_cards[card_name] / self.total_cards

                if not (card_type_prob == 0 and card_prob == 0):
                    cards_into_account += 1
                    probability *= (card_type_prob * card_count / card_prob)

            
                
        probability *= cards_into_account / total_cards
        return probability

    def add_card(self, card):
        self.total_cards += 1
        self.raw_data.append(card)

        hero_class = card['hero_class']
        archetype = card['archetype']
        card_name = card['card_name']
        count = int(card['card_count'])

        if not (card_name in self.all_cards):
            self.all_cards[card_name] = 0.0

        self.all_cards[card_name] += count

        if not archetype in self.archetypes:
            self.archetypes.append(archetype)
        
        if not (hero_class in self.cards):
            self.cards[hero_class] = {}
            self.cards[hero_class]["total"] = 0.0
        if not (archetype in self.cards[hero_class]):
            self.cards[hero_class][archetype] = {}
            self.cards[hero_class][archetype]["total"] = 0.0
        if not (card_name in self.cards[hero_class][archetype]):
            self.cards[hero_class][archetype][card_name] = 0.0

        self.cards[hero_class]["total"] += count
        self.cards[hero_class][archetype]["total"] += count
        self.cards[hero_class][archetype][card_name] += count

    def process_data(self, raw_data):
        for card in raw_data:
            self.add_card(card)

    def classify(self, hero_class, deck):
        type_probability = {}
        total_prob = 0
        for archetype in self.archetypes:
            prob = self.__calculate_probability(hero_class, archetype, deck)
            type_probability[archetype] = prob
            total_prob += prob

        # normalize the probabilities
        if total_prob != 0:
            for archetype in type_probability:
                type_probability[archetype] /= total_prob

        
        return type_probability