from heapq import heappush

class KNearestDecks(object):
    """ Finds the decks that are most similar to a set of cards. """

    MAX_CARDS_IN_DECK = 30

    def __init__(self):
        self.decks = {}

    def update_deck(self, deck_entry):
        """ Adds a card to its corresponding deck. """
        archetype = deck_entry['class'] + '##' + deck_entry['archetype']
        if archetype not in self.decks:
            self.decks[archetype] = {}

        title = deck_entry['title']
        if title not in self.decks[archetype]:
            self.decks[archetype][title] = set()

        self.decks[archetype][title].add(deck_entry['card-name'])

    def get_nearest_decks(self, k, hero_class, archetype, cards):
        """ Finds the k decks that are closest to the passed set of cards. """
        dist_sorted_decks = []
        archetype_id = hero_class + '##' + archetype

        for deck_title, arch_cards in self.decks[archetype_id].iteritems():
            dist = KNearestDecks.__get_distance(arch_cards, cards)
            heappush(dist_sorted_decks, (dist, deck_title))

        return dist_sorted_decks[:k]

    @classmethod
    def __get_distance(cls, first, second):
        return cls.MAX_CARDS_IN_DECK - len(first - second)
