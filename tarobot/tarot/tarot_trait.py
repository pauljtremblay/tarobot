#!/usr/bin/env python3

"""Utility module that contains the tarot trait logic that is later mixed into the TarotCard enumeration."""

from enum import IntEnum
import re

from . archana import Archana
from . card_value import CardValue
from . suit import Suit


class TarotTrait(IntEnum):
    """A trait for all tarot cards, including both major and minor archana."""

    def archana(self):
        """Returns the archana to which this tarot card belongs."""
        return Archana.MAJOR if self.value < 22 else Archana.MINOR

    def suit(self):
        """Returns the suit to which this card belongs, or None in the case of the major archana."""
        if self.archana() == Archana.MAJOR:
            return None
        return Suit((self.value - 22) // 14 + 1)

    def card_value(self):
        """Returns the value of this tarot card, or None in the case of the major archana."""
        if self.archana() == Archana.MAJOR:
            return None
        return CardValue((self.value - 22) % 14 + 1)

    def __str__(self):
        return " ".join(list(map(lambda t: "of" if t == "Of" else t, re.findall('[A-Z][^A-Z]*', self.name))))

    def __repr__(self):
        return "".join(list(map(lambda t: "of" if t == "Of" else t, re.findall('[A-Z][^A-Z]*', self.name))))
