#!/usr/bin/env python3

"""This module contains all the dataclasses used to represent a tarot card reading DTO."""

from dataclasses import dataclass
import json
import re
from typing import ClassVar, Dict, List, Optional

from dataclasses_json import dataclass_json

from . tarot_card import TarotCard


# pylint: disable=C0103,R0902,R0903,R0913,E1101
class AbstractBaseClass:
    """Common ancestor for this module's dataclasses."""


@dataclass
class Metadata(AbstractBaseClass):
    """Stores an openai generate completion request's input and output parameters."""
    openai_id: str
    model: str
    created_ts: int
    # response_ms: int
    max_tokens: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    temperature: Optional[float] = None
    top_p: Optional[float] = None

    def __init__(self, completion):
        self.openai_id = completion.id
        self.model = completion.model
        self.created_ts = completion.created
        # self.response_ms = completion.response_ms
        self.prompt_tokens = completion.usage.prompt_tokens
        self.completion_tokens = completion.usage.completion_tokens
        self.total_tokens = completion.usage.total_tokens


@dataclass_json
@dataclass
class CardReading(AbstractBaseClass):
    """Stores the query, response, and associated metadata for an openai tarot card reading."""
    ignored_parameter_regex: ClassVar[str] = r'card_(list|\d)'
    metadata: Metadata
    spread: List[TarotCard]
    prompt: str
    response: str
    parameters: Optional[Dict[str, str]] = None
    summary: Optional[str] = None

    def __init__(self, completion, spread: List[TarotCard], prompt: str, response: str,
                 parameters: Optional[Dict[str, str]] = None,
                 summary: Optional[str] = None):
        self.metadata = Metadata(completion)
        self.spread = spread
        self.prompt = prompt
        self.response = response
        self.summary = summary
        self.parameters = {}
        if parameters is not None:
            for (param_name, param_value) in parameters.items():
                if re.match(CardReading.ignored_parameter_regex, param_name) is None:
                    self.parameters[param_name] = param_value

    def __str__(self):
        return json.dumps(json.loads(self.to_json()), indent=4)
# pylint: enable=C0103,R0902,R0903,R0913,E1101
