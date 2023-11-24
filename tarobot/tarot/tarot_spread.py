#!/usr/bin/env python3

"""This module contains knowledge about some different common tarot spreads and card layouts."""

from dataclasses import dataclass
from enum import Enum
from inspect import cleandoc
from os.path import dirname, realpath
import re
from typing import Dict, List, Optional, Set

import dataconf

from . tarot_card import TarotCard


class SpreadType(str, Enum):
    """Enumeration representing some common types of Tarot card spreads."""
    ONE_CARD = "one-card"
    CARD_LIST = "card-list"
    TIMELINE = "timeline"
    SITUATION = "situation"
    RELATIONSHIP = "relationship"

    def __str__(self):
        return self.value


@dataclass
class TemplateParameter:
    """DTO representing a required parameter for a template."""
    description: str
    default_value: Optional[str] = None


@dataclass
class SpreadTemplate:
    """DTO representing a tarot card reading's query in terms of the cards, parameters, and message layout."""
    type: SpreadType
    description: str
    roles: Dict[str, str]
    beliefs: Dict[str, str]
    disclaimers: Dict[str, str]
    body: str
    prompt_template: Optional[str] = None
    required_card_count: Optional[int] = None
    required_parameters: Optional[Dict[str, TemplateParameter]] = None


@dataclass
class Spread:
    """DTO representing a Tarot card spread; the type, the cards, additional parameters, and the resulting prompt."""
    spread_type: SpreadType
    tarot_cards: List[TarotCard]
    parameters: Dict[str, str]
    prompt: str


SpreadConfig = Dict[SpreadType, SpreadTemplate]
"""Type alias for the spread type to template dictionary."""


class SpreadBuilder:
    """Service class that transforms a tarot spread request into a prompt-ready package for OpenAI."""

    def __init__(self, location: str = realpath(dirname(dirname(__file__)) + "/config/spreads.conf")):
        spread_types: List[SpreadTemplate] = dataconf.file(location, List[SpreadTemplate])
        self.spread_type_to_template: SpreadConfig = {spread_template.type: spread_template
                                                      for spread_template in spread_types}
        for template in self.spread_type_to_template.values():
            template.description = cleandoc(template.description)
            # assemble the prompt template as a summation of all the roles, beliefs, body, and disclaimers
            template.prompt_template = " ".join(list(template.roles.values()) +
                                                list(template.beliefs.values()) +
                                                [cleandoc(template.body)] +
                                                list(template.disclaimers.values()))

    def build(self, spread_type: SpreadType, tarot_cards: List[TarotCard],
              additional_parameters: Optional[Dict[str, str]] = None) -> Spread:
        """Factory method that builds a Spread DTO for the given spread type, tarot cards, and additional parameters."""
        parameters = {}
        if additional_parameters is not None:
            parameters.update(additional_parameters)
        spread_template: SpreadTemplate = self.spread_type_to_template[spread_type]
        if spread_template.required_card_count is not None:
            _validate_tarot_cards(spread_type, tarot_cards, spread_template.required_card_count)
        if spread_template.required_parameters is not None:
            _validate_spread_parameters(spread_type, parameters, set(spread_template.required_parameters.keys()))
        for n, tarot_card in enumerate(tarot_cards, start=1):
            parameters[f"card_{n}"] = str(tarot_card)
        parameters["card_list"] = ", ".join(str(tarot_card) for tarot_card in tarot_cards)
        return Spread(spread_type=spread_type,
                      tarot_cards=tarot_cards,
                      parameters=parameters,
                      prompt=_replace_tokens(spread_template.prompt_template, parameters))


def _validate_tarot_cards(spread_type: SpreadType, tarot_cards: List[TarotCard], required_card_count: int) -> None:
    """Raises an exception if the tarot card list does not match expectations for the type of tarot spread."""
    if len(tarot_cards) != required_card_count:
        raise ValueError(f"{spread_type} tarot card spread requires exactly {required_card_count} card[s]")


def _validate_spread_parameters(spread_type: SpreadType, parameters: Dict[str, str], required: Set[str]) -> None:
    """Raises an exception if any of the required parameters are missing from the given parameters."""
    if not required.issubset(parameters.keys()):
        missing_params = ", ".join(required.difference(parameters.keys()))
        raise ValueError(f"{spread_type} tarot card spread is missing required parameters {missing_params}")


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
