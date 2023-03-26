#!/usr/bin/env python3

from enum import Enum


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
