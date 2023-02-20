#!/usr/bin/env python3

from enum import Enum

class Archana(Enum):
    """An enumeration representing the different archana."""

    Major = 1
    Minor = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()
