#!/usr/bin/env python3

"""Tarot deck persistence layer.

This module manages storing application data in a relational database.
"""

__all__ = ['session_factory', 'Base', 'CardReadingEntity']

from db.base import session_factory, Base
from db.card_reading_entity import CardReadingEntity
