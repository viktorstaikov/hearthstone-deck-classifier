from heapq import heappush

class KNearestDecks(object):
    """ Finds the decks that are most similar to a set of cards. """

    MAX_CARDS_IN_DECK = 30

    def __init__(self):
        self.decks = {}
        self.card_count = {}

    def update_deck(self, deck_entry):
        """ Adds a card to its corresponding deck. """
        archetype = deck_entry['class'] + '##' + deck_entry['archetype']
        if archetype not in self.decks:
            self.decks[archetype] = {}

        title = deck_entry['title']
        if title not in self.decks[archetype]:
            self.decks[archetype][title] = []

        self.decks[archetype][title].append(deck_entry)

        card_name = deck_entry['card-name']
        deck_entry_id = archetype + '##' + title + '##' + card_name
        self.card_count[deck_entry_id] = int(deck_entry['card-count'])

        print self.decks
        print self.card_count

    def get_nearest_decks(self, k, hero_class, archetypes, cards):
        """ Finds the k decks that are closest to the passed set of cards. """
        dist_sorted_decks = []
        input_card_count = KNearestDecks.__get_count(cards)

        for archetype in archetypes:
            archetype_id = hero_class + '##' + archetype
            for deck_title, deck in self.decks[archetype_id].iteritems():
                deck_id = archetype_id + '##' + deck_title
                dist = self.__get_distance(deck_id, cards)

                if dist == KNearestDecks.MAX_CARDS_IN_DECK:
                    continue

                is_complete_match = KNearestDecks.MAX_CARDS_IN_DECK - dist == input_card_count
                heappush(dist_sorted_decks, (dist, {
                    'deck': deck,
                    'archetype': archetype,
                    'complete_match': is_complete_match
                }))

        return dist_sorted_decks[:k]

    def __get_distance(self, deck_id, cards):
        dist = KNearestDecks.MAX_CARDS_IN_DECK

        for card in cards:
            card_name = card['card-name']
            card_count = int(card['card-count'])
            deck_entry_id = deck_id + '##' + card_name
            if deck_entry_id in self.card_count:
                count_in_deck = self.card_count[deck_entry_id]
                dist -= min(count_in_deck, card_count)

        return dist

    @staticmethod
    def __get_count(cards):
        count = 0
        for card in cards:
            count += int(card['card-count'])
        return count
