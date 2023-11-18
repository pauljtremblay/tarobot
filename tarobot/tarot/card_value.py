#!/usr/bin/env python3

"""This module represents the different card values for all the minor archana cards."""

from enum import IntEnum


class CardValue(IntEnum):
    """An enumeration representing the different card values of a minor archana suit."""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    PAGE = 11
    KNIGHT = 12
    QUEEN = 13
    KING = 14

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name.capitalize()
