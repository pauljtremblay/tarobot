#!/usr/bin/env python3

from enum import Enum
from .tarottrait import TarotTrait
from .suit import Suit
from .cardvalue import CardValue


class TarotCard(TarotTrait, Enum):
    ...


def generate_tarot_cards():
    """generates all tarot cards: the 22 major archana + the 56 minor archana."""
    # major archana
    cards = {
        'TheFool': 0,
        'TheMagician': 1,
        'TheHighPriestess': 2,
        'TheEmpress': 3,
        'TheEmperor': 4,
        'TheHierophant': 5,
        'TheLovers': 6,
        'TheChariot': 7,
        'Justice': 8,
        'TheHermit': 9,
        'TheWheelOfFortune': 10,
        'Strength': 11,
        'TheHangedMan': 12,
        'Death': 13,
        'Temperance': 14,
        'TheDevil': 15,
        'TheTower': 16,
        'TheStar': 17,
        'TheMoon': 18,
        'TheSun': 19,
        'Judgement': 20,
        'TheWorld': 21
    }
    # minor archana
    for s in Suit:
        for cv in CardValue:
            cards["%sOf%s" % (cv, s)] = 21 + 14 * (s.value - 1) + cv.value
    return cards


TarotCard = TarotTrait('TarotCard', generate_tarot_cards())
"""An enumeration representing the 78 cards of a standard tarot deck."""
