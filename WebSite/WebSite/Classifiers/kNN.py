from heapq import heappush

class KNearestNeighbours(object):
    """description of class"""
    def __init__(self):
        self.decks = {}

    def add_card(self, deck_card):
        deck_archetype_id = KNearestNeighbours.__get_deck_archetype_id(
                deck_card['class'], deck_card['archetype'])
        if deck_archetype_id not in self.decks:
            self.decks[deck_archetype_id] = {}

        deck_title = deck_card['title']
        if deck_title not in self.decks[deck_archetype_id]:
            self.decks[deck_archetype_id][deck_title] = set()

        self.decks[deck_archetype_id][deck_title].add(deck_card['card-name'])

    def get_nearest(self, k, hero_class, deck_archetype, deck_cards):
        distSortedDecks = []
        deck_archetype_id = KNearestNeighbours.__get_deck_archetype_id(hero_class, deck_archetype)

        for deck_title, cards in self.decks[deck_archetype_id].iteritems():
            dist = KNearestNeighbours.__get_distance(deck_cards, cards)
            heappush(distSortedDecks, (dist, deck_title))

        print distSortedDecks

    @staticmethod
    def __get_distance(first, second):
        dist = 30
        diff = first - second
        return len(diff)

    @staticmethod
    def __get_deck_archetype_id(hero_class, deck_archetype):
        return '%s##%s' % (hero_class, deck_archetype)


