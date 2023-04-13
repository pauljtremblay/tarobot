#!/usr/bin/env python3

"""This module contains the loader utility that loads tarobot's hocon-based configuration into dataclass objects."""

from dataclasses import dataclass
from os.path import dirname, realpath
from typing import Optional

from dotenv import load_dotenv
import dataconf


# pylint: disable=C0103,R0902,R0903
class AbstractBaseClass:
    """Common ancestor used by app's config dataclasses."""


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
class ConnectionPool(AbstractBaseClass):
    """Data class used for database connection pool config."""
    size: int
    recycle_secs: int
    timeout_secs: int


@dataclass
class Database(AbstractBaseClass):
    """Data class used for storing persistence layer config (db hostname, schema, credentials)."""
    host: str
    port: int
    dialect: str
    driver: str
    schema: str
    user: str
    password: str
    pool: ConnectionPool


@dataclass
class Config(AbstractBaseClass):
    """Data class used for storing the tarobot app's configuration."""
    app_name: str
    openai: OpenAI
    tarot: Tarot
    db: Database
# pylint: enable=C0103,R0902,R0903


class ConfigLoader:  # pylint: disable=R0903
    """Loads the hocon-based config file into a config object."""

    def __init__(self, location):
        # ensure any environment variables found in .env are loaded to make env vars available for variable substitution
        load_dotenv()
        self.config = dataconf.file(location, Config)


# instantiate app config once and use various places: attempt base config if main config fails
CONFIG_PATHS = ["/config/tarobot.conf", "/config/base-tarobot.conf"]
CONFIG: Optional[Config] = None

for path in CONFIG_PATHS:
    if CONFIG is not None:
        break
    try:
        config_path = realpath(dirname(dirname(__file__)) + path)
        CONFIG = ConfigLoader(config_path).config
    except Exception:  # pylint: disable=W0718
        CONFIG = None
