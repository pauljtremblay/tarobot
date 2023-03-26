#!/usr/bin/env python3

from enum import Enum


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
