#!/usr/bin/env python3

"""This module contains all the logic needed to normalize and resolve a given tarot card name into a TarotCard."""

from dataclasses import dataclass
from os.path import realpath, dirname
from typing import Dict, List, Optional

import dataconf

from . card_value import CardValue
from . suit import Suit
from . tarot_card import TarotCard


@dataclass
class AliasConfig:
    """Data class used for storing all tarot card alias information."""
    cards: Dict[str, List[str]]
    suits: Dict[str, List[str]]
    ranks: Dict[str, List[str]]
# pylint: enable=R0903


class CardResolver:
    """Utility class for mapping tarot cards, suits, and values from aliases to their strongly-typed enum values."""

    def __init__(self, location):
        self.aliases = dataconf.file(location, AliasConfig)
        self.card_aliases: Dict[str, TarotCard] = {}
        self.suit_aliases: Dict[str, Suit] = {}
        self.rank_aliases: Dict[str, CardValue] = {}
        # populate "identity" aliases
        for tarot_card in list(TarotCard):
            self.card_aliases[repr(tarot_card).lower()] = tarot_card
        for tarot_suit in list(Suit):
            self.suit_aliases[repr(tarot_suit).lower()] = tarot_suit
        for card_value in list(CardValue):
            self.rank_aliases[repr(card_value).lower()] = card_value
        # populate typed alias -> card map from given config file
        for (card_str, card_aliases) in self.aliases.cards.items():
            tarot_card = TarotCard[card_str]
            for card_alias in card_aliases:
                key = card_alias.lower().replace(" ", "")
                if key in self.card_aliases:
                    raise ValueError(f"duplicate card alias for {key}")
                self.card_aliases[key] = tarot_card
        # populate typed alias -> suit map
        for (suit_str, suit_aliases) in self.aliases.suits.items():
            tarot_suit = Suit[suit_str]
            for suit_alias in suit_aliases:
                key = suit_alias.lower().replace(" ", "")
                if key in self.suit_aliases:
                    raise ValueError(f"duplicate card suit for {key}")
                self.suit_aliases[key] = tarot_suit
        # populate typed alias -> rank map
        for (rank_str, rank_aliases) in self.aliases.ranks.items():
            suit_rank = CardValue[rank_str]
            for rank_alias in rank_aliases:
                key = rank_alias.lower().replace(" ", "")
                if key in self.rank_aliases:
                    raise ValueError(f"duplicate card rank for {key}")
                self.rank_aliases[key] = suit_rank

    def get_card_by_known_alias(self, given_card_name):
        """Normalizes and attempts to resolve the given card into a TarotCard."""
        return self.card_aliases[given_card_name.lower().replace(" ", "")]

    def get_suit_by_known_alias(self, given_suit_name):
        """Normalizes and attempts to resolve the given suit into a Suit."""
        return self.suit_aliases[given_suit_name.lower().replace(" ", "")]

    def get_rank_by_known_alias(self, given_rank_name):
        """Normalizes and attempts to resolve the given cad rank into a CardValue."""
        return self.rank_aliases[given_rank_name.lower().replace(" ", "")]

    def get_optional_card_by_alias(self, given_card_name) -> Optional[TarotCard]:
        """Attempts to resolve the given card name into a TarotCard.

        If no matches can be resolved, then None is returned instead."""
        try:
            # see if the given name is already known
            return self.get_card_by_known_alias(given_card_name)
        except KeyError:
            # card not recognized, if card matches pattern "< rank token >of< suit token >" try to infer card
            alias = given_card_name.lower().replace(" ", "")
            if "of" not in alias:
                return None
            try:
                (rank_alias, suit_alias) = alias.split('of')
                card_value = self.get_rank_by_known_alias(rank_alias)
                suit = self.get_suit_by_known_alias(suit_alias)
                return self.get_card_by_known_alias(f"{card_value}Of{suit}")
            except KeyError:
                return None


# instantiate app config once and use various places
aliases_path = realpath(dirname(dirname(__file__)) + "/config/aliases.conf")
resolver: CardResolver = CardResolver(aliases_path)
