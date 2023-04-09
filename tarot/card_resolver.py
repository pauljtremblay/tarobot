#!/usr/bin/env python3

from dataclasses import dataclass
import dataconf
from os.path import realpath, dirname
from typing import Dict, List, Optional

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
                key = alias.lower().replace(" ", "")
                if key in self.card_aliases:
                    raise ValueError("duplicate card alias for {}".format(key))
                self.card_aliases[key] = tarot_card
        # populate typed alias -> suit map
        for (suit_str, aliases) in self.config.suit_aliases.items():
            tarot_suit = Suit[suit_str]
            for alias in aliases:
                key = alias.lower().replace(" ", "")
                if key in self.suit_aliases:
                    raise ValueError("duplicate card suit for {}".format(key))
                self.suit_aliases[key] = tarot_suit
        # populate typed alias -> rank map
        for (rank_str, aliases) in self.config.rank_aliases.items():
            suit_rank = CardValue[rank_str]
            for alias in aliases:
                key = alias.lower().replace(" ", "")
                if key in self.rank_aliases:
                    raise ValueError("duplicate card rank for {}".format(key))
                self.rank_aliases[key] = suit_rank

    def get_card_by_known_alias(self, given_card_name):
        return self.card_aliases[given_card_name.lower().replace(" ", "")]

    def get_suit_by_known_alias(self, given_suit_name):
        return self.suit_aliases[given_suit_name.lower().replace(" ", "")]

    def get_rank_by_known_alias(self, given_rank_name):
        return self.rank_aliases[given_rank_name.lower().replace(" ", "")]

    def get_optional_card_by_alias(self, given_card_name) -> Optional[TarotCard]:
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
                return self.get_card_by_known_alias("{}Of{}".format(card_value, suit))
            except KeyError:
                return None


# instantiate app config once and use various places
aliases_path = realpath(dirname(dirname(__file__)) + "/config/aliases.conf")
resolver: CardResolver = CardResolver(aliases_path)
