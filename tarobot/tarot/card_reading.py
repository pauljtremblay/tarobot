#!/usr/bin/env python3

from dataclasses import dataclass
import json
from typing import List, Optional

from dataclasses_json import dataclass_json
from openai import Completion

from . import TarotCard


class AbstractBaseClass:
    pass


@dataclass
class Metadata(AbstractBaseClass):
    """Stores an openai generate completion request's input and output parameters."""
    openai_id: str
    model: str
    created_ts: int
    response_ms: int
    max_tokens: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    temperature: Optional[float] = None
    top_p: Optional[float] = None

    def __init__(self, completion: Completion):
        self.openai_id = completion.openai_id
        self.model = completion.model
        self.created_ts = completion.created
        self.response_ms = completion.response_ms
        self.prompt_tokens = completion['usage']['prompt_tokens']
        self.completion_tokens = completion['usage']['completion_tokens']
        self.total_tokens = completion['usage']['total_tokens']


@dataclass_json
@dataclass
class CardReading(AbstractBaseClass):
    """Stores the query, response, and associated metadata for an openai tarot card reading."""
    metadata: Metadata
    spread: List[TarotCard]
    prompt: str
    response: str
    subject: str
    teller: Optional[str]

    def __init__(self, completion: Completion, spread: List[TarotCard], prompt, response, subject, teller=None):
        self.metadata = Metadata(completion)
        self.spread = spread
        self.prompt = prompt
        self.response = response
        self.subject = subject
        self.teller = teller

    def __str__(self):
        return json.dumps(json.loads(self.to_json()), indent=4)
