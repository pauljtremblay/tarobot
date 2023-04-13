#!/usr/bin/env python3

"""This module contains tarobot's core application logic."""

from argparse import ArgumentError
import logging
import sys
from typing import Optional

import openai

from .. db import session_factory, CardReadingEntity
from .. tarot import TarotDeck, CardReading
from . command_parser import CommandParser
from . config import CONFIG, Config


logger = logging.getLogger(__name__)


class App:
    """This class processes input from command line arguments and executes the request."""

    def __init__(self, config_opt: Optional[Config] = None):
        # load app config
        if config_opt is not None:
            self.__config = config_opt
        else:
            self.__config = CONFIG
        # initialize openai module, or error out if api key is not defined
        openai.api_key = self.__config.openai.api_key
        self.parser = CommandParser(self.__config)
        self.command = None
        self.spread = None

    def main(self):
        """The main method: draws 3 tarot cards at random and has openai generate a tarot card reading."""
        try:
            self.command = self.parser.parse_command_line_args(sys.argv[1:])
        except ArgumentError as arg_error:
            # exits the app with an error code and a formatted message
            self.parser.print_parse_error_and_exit(arg_error)
        except ValueError:
            # log an error and exits the app
            logger.fatal("Fatal error processing command line args", exc_info=True)
            sys.exit(1)
        self.create_tarot_spread()
        self.interpret_tarot_spread()

    def create_tarot_spread(self):
        """Creates a tarot spread from either the given cards or a locally created tarot card deck."""
        if self.command.given_cards is not None:
            self.spread = self.command.given_cards
        else:
            deck = TarotDeck()
            self.spread = deck.draw(self.command.card_count)

    def interpret_tarot_spread(self):
        """Generates a tarot card reading for the given spread and prints to standard output."""
        spread_str = ", ".join(str(card) for card in self.spread)
        logger.info("Generating a tarot card reading for %s for the following spread:\n\t%s\n",
                    self.command.subject, spread_str)
        tarot_reading_prompt = self.generate_tarot_reading_prompt()
        if self.command.show_prompt:
            logger.info("Prompt:\n%s\n", tarot_reading_prompt)
        card_reading = self.ask_openai_to_generate_card_reading(tarot_reading_prompt)
        card_reading.metadata.max_tokens = self.__config.openai.completion.max_tokens
        logger.info("Response:\n%s", card_reading.response)
        if self.command.show_diagnostics:
            logger.debug("\n[ diagnostics ]\n%s\n", card_reading)
        if self.command.persist_reading:
            persist_card_reading(card_reading)

    def generate_tarot_reading_prompt(self):
        """Generates the prompt to openai for how to generate a tarot card reading for the given spread."""
        prompt = f"Tarot card reading for {self.command.subject} with the cards "
        if len(self.spread) < 2:
            prompt += self.spread[0]
        else:
            [*head, tail] = self.spread
            prompt += ", ".join(str(card) for card in head) + ", and " + str(tail)
        if self.command.teller is not None:
            prompt += " in the style of " + self.command.teller
        return prompt

    def ask_openai_to_generate_card_reading(self, prompt):
        """Displays the prompt to and associated response from openai."""
        completion_config = self.__config.openai.completion
        completion_kwargs = {
            'model': completion_config.model,
            'max_tokens': completion_config.max_tokens,
            'prompt': prompt
        }
        if completion_config.n is not None:
            completion_kwargs['n'] = completion_config.n
        if completion_config.temperature is not None:
            completion_kwargs['temperature'] = completion_config.temperature
        if completion_config.top_p is not None:
            completion_kwargs['top_p'] = completion_config.top_p
        completion = openai.Completion.create(**completion_kwargs)
        response = "\n".join(list(choice.text for choice in completion.choices)).strip()
        command = self.command
        card_reading = CardReading(completion, self.spread, prompt, response, command.subject, command.teller)
        if 'temperature' in completion_kwargs:
            card_reading.metadata.temperature = completion_kwargs['temperature']
        if 'top_p' in completion_kwargs:
            card_reading.metadata.top_p = completion_kwargs['top_p']
        return card_reading


def persist_card_reading(card_reading_dto: CardReading):
    """Records the details of the tarot card reading.

    This includes the inputs: the subject, the teller, the tarot card spread, resulting response, and response metadata.
    If the app fails to connect to the database, then an error is printed to stderr.
    """
    try:
        session = session_factory()
        with session.begin():
            session.add(CardReadingEntity(card_reading_dto))
    except Exception:  # pylint: disable=W0718
        logger.error("Failed to record card reading in the database", exc_info=True)
