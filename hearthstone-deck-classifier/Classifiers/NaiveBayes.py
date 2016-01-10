class NaiveBayes(object):
    """Naive Bayes Classifier for the purpose of classifying Hearthstone Decks"""

    def __init__(self):
        self.total_cards = 0
        self.raw_data = []
        self.data = {}
        self.cards = {}

    def ProcessData(self, raw_data):
        self.raw_data = raw_data
        self.total_cards = len(raw_data)

        for card in raw_data:
            hero_class = card["class"]
            type = card["archetype"]
            card_name = card["card-name"]

            if not (card_name in self.cards):
                self.cards[card_name] = 0

            self.cards[card_name] += 1


            if not (hero_class in self.data):
                self.data[hero_class] = {}
                self.data[hero_class]["total"] = 0
            if not (type in self.data[hero_class]):
                self.data[hero_class][type] = {}
                self.data[hero_class][type]["total"] = 0
            if not (card_name in self.data[hero_class][type]):
                self.data[hero_class][archetype][card_name] = 0

            self.data[hero_class]["total"] += 1
            self.data[hero_class][type]["total"] += 1
            self.data[hero_class][archetype][card_name] += 1
