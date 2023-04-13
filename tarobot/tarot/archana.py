#!/usr/bin/env python3

"""Module containing the major/minor archana enumeration."""

from enum import Enum


class Archana(Enum):
    """An enumeration representing the different archana."""

    MAJOR = 1
    MINOR = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name.capitalize()
