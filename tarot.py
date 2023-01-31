#!/usr/bin/env python3

from enum import Enum
import random
import re



"""This module models the structure and behavior of a 78 card tarot deck. A tarot deck consists of
78 cards: the 22 cards from the major archana, and the 56 cards from the minor archana. The minor
archana consists of 4 suites (Wands, Cups, Swords, and Pentacles). Each suit of the minor archana
has 14 cards, Ace through Ten, and 4 face cards: Page, Knight, Queen, and King."""


class Archana(Enum):
    """An enumeration representing the different archana."""
    
    Major = 1
    Minor = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class Suit(Enum):
    """An enumeration representing the different suits of the minor archana."""
    
    Wands = 1
    Cups = 2
    Swords = 3
    Pentacles = 4

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class CardValue(Enum):
    """An enumeration representing the different card values of a minor archana suit."""
    
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Page = 11
    Knight = 12
    Queen = 13
    King = 14

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class TarotCard(Enum):
    """A parent class of both major and minor archana enumerations."""

    def archana(self):
        """Returns the archana to which this tarot card belongs."""
        return Archana.Major if self.value < 22 else Archana.Minor

    def suit(self):
        """Returns the suit to which this tarot card belongs, or None in the case of the major archana."""
        if self.archana() == Archana.Major:
            return None
        return Suit((self.value - len(MajorArchana)) // len(CardValue) + 1)

    def card_value(self):
        """Returns the value of this tarot card, or None in the case of the major archana."""
        if self.archana() == Archana.Major:
            return None
        return CardValue((self.value - len(MajorArchana)) % len(CardValue) + 1)

    def __repr__(self):
        return " ".join(list(map(lambda t: "of" if t == "Of" else t, re.findall('[A-Z][^A-Z]*', self.name))))

    def __str__(self):
        return self.__repr__()


class MajorArchana(TarotCard):
    """An enumeration representing the 22 cards of the major archana."""
    
    TheFool = 0
    TheMagician = 1
    TheHighPriestess = 2
    TheEmpress = 3
    TheEmperor = 4
    TheHierophant = 5
    TheLovers = 6
    TheChariot = 7
    Justice = 8
    TheHermit = 9
    TheWheelOfFortune = 10
    Strength = 11
    TheHangedMan = 12
    Death = 13
    Temperance = 14
    TheDevil = 15
    TheTower = 16
    TheStar = 17
    TheMoon = 18
    TheSun = 19
    Judgement = 20
    TheWorld = 21


def generate_minor_archana():
    """generator for the minor archana: 4 suits x 14 card values."""
    cards = {}
    for s in Suit:
        for cv in CardValue:
            cards["%sOf%s" % (cv, s)] = len(MajorArchana) + len(CardValue) * (s.value - 1) + cv.value - 1
    return cards


MinorArchana = TarotCard('MinorArchana', generate_minor_archana())
    """An enumeration representing the 56 cards of the minor archana."""


class TarotDeck:
    """Model that represents a shuffled tarot card deck."""

    def __init__(self):
        self.cards = list(MajorArchana) + list(MinorArchana)
        # always shuffle the tarot deck before use
        random.shuffle(self.cards)

    def draw(self, count):
        """Returns the requested count of cards from the shuffled tarot card deck."""
        drawn = []
        for i in range(count):
            drawn.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
        return drawn
