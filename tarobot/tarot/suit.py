#!/usr/bin/env python3

"""Module that represents for the four different suits of the minor archana."""

from enum import IntEnum


class Suit(IntEnum):
    """An enumeration representing the different suits of the minor archana."""

    WANDS = 1
    CUPS = 2
    SWORDS = 3
    PENTACLES = 4

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name.capitalize()
