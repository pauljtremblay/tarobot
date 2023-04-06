#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import dataconf


class AbstractBaseClass:
    pass


@dataclass
class Completion(AbstractBaseClass):
    """OpenAI completion api request configuration."""
    model: str
    max_tokens: int = 2048
    n: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


@dataclass
class OpenAI(AbstractBaseClass):
    """Data class used for storing all openai-related configuration."""
    api_key: str
    completion: Completion


@dataclass
class Tarot(AbstractBaseClass):
    """Data class used for storing tarot-related configuration."""
    min_cards: int
    max_cards: int
    default_cards: int


@dataclass
class Config(AbstractBaseClass):
    """Data class used for storing the tarobot app's configuration."""
    app_name: str
    openai: OpenAI
    tarot: Tarot


class ConfigLoader:
    """Loads the hocon-based config file into a config object."""

    def __init__(self, location):
        # ensure any environment variables found in .env are loaded to make env vars available for variable substitution
        load_dotenv()
        self.config = dataconf.file(location, Config)