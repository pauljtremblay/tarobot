#!/usr/bin/env python3

"""Module containing the tarot deck card management logic."""

import random

from . tarot_card import TarotCard


# pylint: disable=R0903
class TarotDeck:
    """Model that represents a shuffled tarot card deck."""

    def __init__(self):
        self.cards = list(TarotCard)
        # always shuffle the tarot deck before use
        random.shuffle(self.cards)

    def draw(self, count):
        """Returns the requested count of cards from the shuffled tarot card deck."""
        drawn = []
        for _ in range(count):
            drawn.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
        return drawn
# pylint: enable=R0903
