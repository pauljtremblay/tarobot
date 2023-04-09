#!/usr/bin/env python3

"""Tarot deck persistence layer.

This module manages storing application data in a relational database.
"""

__all__ = ['Base', 'CardReadingEntity']

from db.base import Base
from db.card_reading_entity import CardReadingEntity
