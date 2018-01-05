from .card import *
from .minion import Minion
from .spell import Spell
from .hero import Hero
import random


class Deck:
    def __init__(self, pclass, cards={}):
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
        if isinstance(cards, dict):
            mycards = cards

        elif (isinstance(cards, list)
              or isinstance(cards, tuple)):
            mycards = {}
            for i in cards:
                mycards[i[0]] = i[1]

        self.create_deck(mycards)

    def create_deck(self, cards):
        self.deck = []
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

            """
            new_card.register_prop('in_deck', True)
            new_card.register_prop('in_hand', False)
            new_card.register_prop('in_graveyard', False)
            if not isinstance(new_card, Spell):
                new_card.register_prop('on_battlefield', False)
            self.deck.append(new_card)"""
            self.put_card_on_index(new_card, 0)

        random.shuffle(self.deck)

    def draw_card(self):
        c = self.deck.pop()
        c.change_prop('in_deck', False)
        c.change_prop('in_hand', True)
        return c

    def shuffle_card(self, card):
        """card: Card instance"""
        i = random.randint(0, len(self.deck)+1)
        put_card_on_index(card, i)

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
        for i in range(numcards):
            self.draw()

    def draw(self):
        self.add_card_to_hand(self.deck.draw_card())

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def __getitem__(self, index):
        return self.hand[index]
