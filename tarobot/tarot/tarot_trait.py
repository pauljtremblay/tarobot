#!/usr/bin/env python3

from enum import Enum
import re

from . archana import Archana
from . card_value import CardValue
from . suit import Suit


class TarotTrait(Enum):
    """A trait for all tarot cards, including both major and minor archana."""

    def archana(self):
        """Returns the archana to which this tarot card belongs."""
        return Archana.Major if self.value < 22 else Archana.Minor

    def suit(self):
        """Returns the suit to which this card belongs, or None in the case of the major archana."""
        if self.archana() == Archana.Major:
            return None
        return Suit((self.value - 22) // 14 + 1)

    def card_value(self):
        """Returns the value of this tarot card, or None in the case of the major archana."""
        if self.archana() == Archana.Major:
            return None
        return CardValue((self.value - 22) % 14 + 1)

    def __str__(self):
        return " ".join(list(map(lambda t: "of" if t == "Of" else t, re.findall('[A-Z][^A-Z]*', self.name))))

    def __repr__(self):
        return "".join(list(map(lambda t: "of" if t == "Of" else t, re.findall('[A-Z][^A-Z]*', self.name))))
