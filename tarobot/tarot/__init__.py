#!/usr/bin/env python3

"""Tarot deck module for card games and cartomancy

This module models the structure and behavior of a 78 card tarot deck. A tarot deck consists of
78 cards: the 22 cards from the major archana, and the 56 cards from the minor archana. The minor
archana consists of 4 suites (Wands, Cups, Swords, and Pentacles). Each suit of the minor archana
has 14 cards, Ace through Ten, and 4 face cards: Page, Knight, Queen, and King.
"""

__all__ = ['Archana', 'Suit', 'CardValue', 'TarotCard', 'TarotDeck', 'resolver', 'CardResolver', 'CardReading']

from tarobot.tarot.archana import Archana
from tarobot.tarot.suit import Suit
from tarobot.tarot.card_value import CardValue
from tarobot.tarot.tarot_card import TarotCard
from tarobot.tarot.deck import TarotDeck
from tarobot.tarot.card_resolver import resolver, CardResolver
from tarobot.tarot.card_reading import CardReading
