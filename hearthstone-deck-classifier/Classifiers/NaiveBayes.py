class NaiveBayes(object):
    """Naive Bayes Classifier for the purpose of classifying Hearthstone Decks"""

    def __init__(self):
        self.total_cards = 0
        self.raw_data = []
        self.cards = {}
        self.all_cards = {}
        self.classes = []
        self.archetypes = []

    def __CalculateProbability(self, hero_class, archetype, deck):

        if not archetype in self.cards[hero_class]:
            return 0


        # the number of cards is proportional on the number of decks
        probability = 1.0
        probability *= self.cards[hero_class][archetype]["total"] / self.cards[hero_class]["total"]

        for card in deck:
            card_name = card["card-name"]

            if not card_name in self.cards[hero_class][archetype]:
                return 0

            # numerator 
            card_type_prob = self.cards[hero_class][archetype][card_name] / self.cards[hero_class][archetype]["total"]
            # denominator
            card_prob = self.all_cards[card_name] / self.total_cards

            if card_type_prob == 0 or card_prob == 0:
                return 0

            probability *= (card_type_prob / card_prob)
                

        return probability

    def AddCard(self, card):
        self.total_cards += 1
        self.raw_data.append(card)

        hero_class = card["class"]
        archetype = card["archetype"]
        card_name = card["card-name"]
        count = int(card["card-count"])

        if not (card_name in self.all_cards):
            self.all_cards[card_name] = 0.0

        self.all_cards[card_name] += count
        
        if not (hero_class in self.cards):
            self.cards[hero_class] = {}
            self.cards[hero_class]["total"] = 0.0
            
            #self.classes.append(hero_class)

        if not (archetype in self.cards[hero_class]):
            self.cards[hero_class][archetype] = {}
            self.cards[hero_class][archetype]["total"] = 0.0
            self.archetypes.append(archetype)

        if not (card_name in self.cards[hero_class][archetype]):
            self.cards[hero_class][archetype][card_name] = 0.0

        self.cards[hero_class]["total"] += count
        self.cards[hero_class][archetype]["total"] += count
        self.cards[hero_class][archetype][card_name] += count

    def ProcessData(self, raw_data):
        for card in raw_data:
            self.AddCard(card)

    def Classify(self, hero_class, deck):
        max_prob = 0.0
        most_prob = "unknown"
        for archetype in self.archetypes:
            prob = self.__CalculateProbability(hero_class, archetype, deck)
            if prob > max_prob:
                max_prob = prob
                most_prob = archetype
        
        return most_prob