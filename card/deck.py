import random
from .card import Card, TYPES
from .minion import Minion
from .spell import Spell
from .hero import Hero


class Deck:
    def __init__(self, pclass, cards=()):
        """
        cards: dict/list of tuples that resembles cards with effects&stuff
        \tformat: {`card_name`:
        \t\t{`type`: type (as index of card.TYPES),
        \t\t 'dmg': x,
        \t\t 'mana': y,
        \t\t 'effects': [(`trigger1`, 'dostuff'),...]...},...}
        \t[(`card_name`, {...}),...]
        """
        self.pclass = pclass
        mycards = cards
        self.create_deck(mycards)

    def create_deck(self, cards):
        self.deck = []
        if isinstance(cards, dict):
            for i in cards.keys():
                mana = cards[i]['mana']
                cclass = cards[i]['cclass']
                if TYPES[cards[i]['type']] == 'spell':
                    effect = cards[i]['effect']

                    new_card = Spell(i, mana, effect, cclass)

                elif TYPES[cards[i]['type']] == 'minion':
                    hp = cards[i]['hp']
                    dmg = cards[i]['dmg']
                    try:
                        abilities = cards[i]['effects']
                    except KeyError:
                        abilities = {}

                        new_card = Minion(i, mana, hp, dmg, cclass, abilities)

                elif TYPES[cards[i]['type']] == 'hero':
                    hp = cards[i]['hp']
                    effect = cards[i]['effect']

                    new_card = Hero(i, mana, cclass, hp, effect)

                self.put_card_on_index(new_card, 0)

        else:
            for i in cards:
                if isinstance(i, Card):
                    self.put_card_on_index(i, 0)
                    continue
                cname = i[0]
                cprops = i[1]

                mana = cprops['mana']
                cclass = cprops['cclass']
                if TYPES[cprops['type']] == 'spell':
                    effect = cprops['effect']

                    new_card = Spell(cname, mana, effect, cclass)

                elif TYPES[cprops['type']] == 'minion':
                    hp = cprops['hp']
                    dmg = cprops['dmg']
                    try:
                        abilities = cprops['effects']
                    except KeyError:
                        abilities = {}

                    new_card = Minion(cname, mana, hp, dmg, cclass, abilities)

                elif TYPES[cprops['type']] == 'hero':
                    hp = cprops['hp']
                    effect = cprops['effect']

                    new_card = Hero(cname, mana, cclass, hp, effect)

                self.put_card_on_index(new_card, 0)

        random.shuffle(self.deck)

    def draw_cards(self, cnt=1):
        cards = []
        while cnt > 0:
            # assert len(self.deck) > 0, self.deck
            c = self.deck.pop()
            c.set_prop('in_deck', False)
            c.set_prop('in_hand', True)
            cards.append(c)
            cnt -= 1
        return cards

    def shuffle_card(self, card):
        """card: Card instance"""
        i = random.randint(0, len(self.deck)+1)
        self.put_card_on_index(card, i)

    def put_card_on_index(self, card, index=0):
        if isinstance(card, Card):
            self.deck.insert(index, card)
            card.register_prop('in_deck', True)
            card.register_prop('in_hand', False)
            card.register_prop('in_graveyard', False)
            if not isinstance(card, Spell):
                card.register_prop('on_battlefield', False)
        else:
            raise TypeError('tried to add non-card to deck')

    def show_card(self, ctype=''):
        if ctype in ('', '*'):
            return random.choice(self.deck)
        if ctype.lower() in ('spell', 's', TYPES.index('spell')):
            # make a collection of all spells in the deck
            s = []
            for i in self.deck:
                if isinstance(i, Spell):
                    s.append(i)
            return random.choice(s)
        if ctype.lower() in ('minion', 'm', TYPES.index('minion')):
            # make a collection of all minions in the deck
            m = []
            for i in self.deck:
                if isinstance(i, Minion):
                    m.append(i)
            return random.choice(m)
        if ctype.lower() in ('hero', 'h', TYPES.index('hero')):
            h = []
            for i in self.deck:
                if isinstance(i, Hero):
                    h.append(i)
            return random.choice(h)

    def __len__(self):
        return len(self.deck)


class Hand:
    def __init__(self, deck, numcards=3):
        """numcards: number of cards to draw\ndeck: deck from which to draw"""
        self.deck = deck
        self.hand = []
        self.draw(numcards)

    def draw(self, cnt):
        self.add_card_to_hand(self.deck.draw_cards(cnt))

    def add_card_to_hand(self, cards):
        if isinstance(cards, (list, tuple)):
            self.hand.extend(cards)
        else:
            self.hand.append(cards)

    def __getitem__(self, index):
        return self.hand[index]
