#!/usr/bin/env python3

"""Tarot deck persistence layer.

This module manages storing application data in a relational database.
"""

__all__ = ['session_factory', 'CardReadingEntity']

from . base import session_factory
from . card_reading_entity import CardReadingEntity
