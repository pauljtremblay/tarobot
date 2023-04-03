#!/usr/bin/env python3

from dataclasses import dataclass
import dataconf
from typing import Dict, List
from .card_value import CardValue
from .suit import Suit
from .tarot_card import TarotCard


class AbstractBaseClass:
    pass


@dataclass
class AliasConfig(AbstractBaseClass):
    """Data class used for storing all tarot card alias information."""
    card_aliases: Dict[str, List[str]]
    suit_aliases: Dict[str, List[str]]
    rank_aliases: Dict[str, List[str]]


class CardResolver:
    """Utility class for mapping tarot cards, suits, and values from aliases to their strongly-typed enum values."""

    def __init__(self, location):
        self.config = dataconf.file(location, AliasConfig)
        self.card_aliases: Dict[str, TarotCard] = dict()
        self.suit_aliases: Dict[str, Suit] = dict()
        self.rank_aliases: Dict[str, CardValue] = dict()
        # populate "identity" aliases
        for tarot_card in list(TarotCard):
            self.card_aliases[repr(tarot_card).lower()] = tarot_card
        for tarot_suit in list(Suit):
            self.suit_aliases[repr(tarot_suit).lower()] = tarot_suit
        for card_value in list(CardValue):
            self.rank_aliases[repr(card_value).lower()] = card_value
        # populate typed alias -> card map from given config file
        for (card_str, aliases) in self.config.card_aliases.items():
            tarot_card = TarotCard[card_str]
            for alias in aliases:
                key = alias.lower()
                if key in self.card_aliases:
                    raise ValueError("duplicate card alias for {}".format(key))
                self.card_aliases[key] = tarot_card
        # populate typed alias -> suit map
        for (suit_str, aliases) in self.config.suit_aliases.items():
            tarot_suit = Suit[suit_str]
            for alias in aliases:
                key = alias.lower()
                if key in self.suit_aliases:
                    raise ValueError("duplicate card suit for {}".format(key))
                self.suit_aliases[key] = tarot_suit
        # populate typed alias -> rank map
        for (rank_str, aliases) in self.config.rank_aliases.items():
            suit_rank = CardValue[rank_str]
            for alias in aliases:
                key = alias.lower()
                if key in self.rank_aliases:
                    raise ValueError("duplicate card rank for {}".format(key))
                self.rank_aliases[key] = suit_rank
        print(self.rank_aliases)

    def get_card_by_alias(self, card_name):
        return self.card_aliases[card_name.lower()]

    def get_suit_by_alias(self, suit_name):
        return self.suit_aliases[suit_name.lower()]

    def get_rank_by_alias(self, rank_name):
        return self.rank_aliases[rank_name.lower()]
