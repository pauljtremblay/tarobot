#!/usr/bin/env python3

"""Module containing the major/minor archana enumeration."""

from enum import Enum


class Archana(str, Enum):
    """An enumeration representing the different archana."""

    MAJOR = "major"
    MINOR = "minor"
