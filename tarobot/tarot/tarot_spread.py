#!/usr/bin/env python3

"""This module contains knowledge about some different common tarot spreads and card layouts."""

from dataclasses import dataclass
from enum import Enum
from inspect import cleandoc
from os.path import dirname, realpath
import re
from typing import Dict, List, Optional

import dataconf

from . tarot_card import TarotCard


class SpreadType(str, Enum):
    """Enumeration representing some common types of Tarot card spreads."""
    ONE_CARD = "one-card"
    CARD_LIST = "card-list"
    PAST_PRESENT_FUTURE = "past-present-future"
    SITUATION_OBSTACLE_ADVICE = "situation-obstacle-advice"
    SEEKER_SUBJECT_RELATIONSHIP = "seeker-subject-relationship"

    def __str__(self):
        return self.value


@dataclass
class SpreadLayout:
    """DTO representing a tarot card reading's query in terms of the cards and parameters."""
    description: str
    template: str


@dataclass
class Spread:
    """DTO representing a Tarot card spread; the type, the cards, additional parameters, and the resulting prompt."""
    spread_type: SpreadType
    tarot_cards: List[TarotCard]
    parameters: Dict[str, str]
    prompt: str


SpreadConfig = Dict[SpreadType, SpreadLayout]
"""Type alias for the spread type to layout dictionary."""


class SpreadBuilder:
    """Service that builds Tarot spread DTOs and prompts for the given parameters."""
    def __init__(self, location: str = realpath(dirname(dirname(__file__)) + "/config/spreads.conf")):
        spread_config: SpreadConfig = dataconf.file(location, SpreadConfig)
        self.type_to_template: Dict[SpreadType, str] = {spread_type: cleandoc(layout.template)
                                                        for (spread_type, layout) in spread_config.items()}

    def build(self, spread_type: SpreadType, tarot_cards: List[TarotCard],
              additional_parameters: Optional[Dict[str, str]] = None) -> Spread:
        """Factory method that builds a Spread DTO for the given spread type, tarot cards, and additional parameters."""
        parameters = {}
        if additional_parameters is not None:
            parameters.update(additional_parameters)
        match spread_type:
            case SpreadType.ONE_CARD:
                return self._for_one_card(tarot_cards)
            case SpreadType.CARD_LIST:
                return self._for_card_list(tarot_cards, **parameters)
            case SpreadType.PAST_PRESENT_FUTURE:
                return self._for_past_present_future(tarot_cards)
            case SpreadType.SEEKER_SUBJECT_RELATIONSHIP:
                return self._for_seeker_subject_relationship(tarot_cards)
            case SpreadType.SITUATION_OBSTACLE_ADVICE:
                return self._for_situation_obstacle_advice(tarot_cards, **parameters)

    def _for_one_card(self, tarot_cards: List[TarotCard]) -> Spread:
        """Builds a simple Tarot spread around a single card."""
        spread_type = SpreadType.ONE_CARD
        _validate_tarot_cards(spread_type, tarot_cards, 1)
        parameters = {'card_1': str(tarot_cards[0])}
        return self._to_spread(spread_type, tarot_cards, parameters)

    def _for_card_list(self, tarot_cards: List[TarotCard], seeker: str, teller: str) -> Spread:
        """Builds a spread around a variable number of cards, a seeker (querent), and fortune teller."""
        parameters = {'seeker': seeker, 'teller': teller, 'card_list': ', '.join(str(card) for card in tarot_cards)}
        return self._to_spread(SpreadType.CARD_LIST, tarot_cards, parameters)

    def _for_past_present_future(self, tarot_cards: List[TarotCard]) -> Spread:
        """Builds a spread around 3 cards representing the past, present, and future for the querent."""
        spread_type = SpreadType.PAST_PRESENT_FUTURE
        _validate_tarot_cards(spread_type, tarot_cards, 3)
        parameters = {'card_1': str(tarot_cards[0]), 'card_2': str(tarot_cards[1]), 'card_3': str(tarot_cards[2])}
        return self._to_spread(spread_type, tarot_cards, parameters)

    def _for_seeker_subject_relationship(self, tarot_cards: List[TarotCard]) -> Spread:
        """Builds a spread around 3 cards representing the querent, subject, and their relationship."""
        spread_type = SpreadType.SEEKER_SUBJECT_RELATIONSHIP
        _validate_tarot_cards(spread_type, tarot_cards, 3)
        parameters = {'card_1': str(tarot_cards[0]), 'card_2': str(tarot_cards[1]), 'card_3': str(tarot_cards[2])}
        return self._to_spread(spread_type, tarot_cards, parameters)

    def _for_situation_obstacle_advice(self, tarot_cards: List[TarotCard], situation: str,  obstacle: str) -> Spread:
        """Builds a spread around 3 cards representing a situation, an obstacle, and advice for the querent."""
        spread_type = SpreadType.SITUATION_OBSTACLE_ADVICE
        _validate_tarot_cards(spread_type, tarot_cards, 3)
        parameters = {'card_1': str(tarot_cards[0]), 'card_2': str(tarot_cards[1]), 'card_3': str(tarot_cards[2]),
                      'situation': situation, 'obstacle': obstacle}
        return self._to_spread(spread_type, tarot_cards, parameters)

    def _to_spread(self, spread_type: SpreadType, tarot_cards: List[TarotCard], parameters: Dict[str, str]) -> Spread:
        """Constructs a spread DTO object for the given spread type, tarot cards, and prompt parameters."""
        return Spread(spread_type=spread_type,
                      tarot_cards=tarot_cards,
                      parameters=parameters,
                      prompt=_replace_tokens(self.type_to_template[spread_type], parameters))


def _validate_tarot_cards(spread_type: SpreadType, tarot_cards: List[TarotCard], required_card_count: int):
    """Raises an exception if the tarot card list does not match expectations for the type of tarot spread."""
    if len(tarot_cards) != required_card_count:
        raise ValueError(f"{spread_type} tarot card spread expects exactly {required_card_count} card[s]")


def _replace_tokens(template: str, replacements: Dict[str, str]) -> str:
    """Replaces all placeholder tokens with their replacement value in the prompt template, not unlike "mad libs".

    Raises ValueError if any placeholder tokens remain empty."""
    # normalize whitespace: filter out newlines and redundant spaces
    prompt = template
    prompt = prompt.replace('\n', ' ')
    prompt = re.sub(r'\s{2,}', ' ', prompt)
    # replace all placeholder tokens with their replacement value
    for (token, replacement) in replacements.items():
        prompt = prompt.replace(f'[{token}]', replacement)
    # raise an exception if there are any remaining placeholder tokens
    leftover_token_match = re.search(r'\[(.+)]', prompt)
    if leftover_token_match is not None:
        raise ValueError(f'Prompt template still has empty token "{leftover_token_match.group(1)}"')
    return prompt.strip()


spread_builder: SpreadBuilder = SpreadBuilder()
