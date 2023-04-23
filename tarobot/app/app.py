#!/usr/bin/env python3

"""This module contains tarobot's core application logic."""

from argparse import ArgumentError
import logging
import sys
from typing import Optional

import openai

from .. db import session_factory, CardReadingEntity
from .. tarot import TarotDeck, CardReading
from .. tarot.card_reading import Metadata
from . command_parser import CommandParser
from . config import Completion, CONFIG, Config


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
        card_reading = self.interpret_tarot_spread()
        if self.command.show_diagnostics:
            logger.debug("\n[ diagnostics ]\n%s\n", card_reading)
        if self.command.persist_reading:
            persist_card_reading(card_reading)

    def create_tarot_spread(self):
        """Creates a tarot spread from either the given cards or a locally created tarot card deck."""
        if self.command.given_cards is not None:
            self.spread = self.command.given_cards
        else:
            deck = TarotDeck()
            self.spread = deck.draw(self.command.card_count)

    def interpret_tarot_spread(self):
        """Generates a tarot card reading for the given spread and logs the response."""
        spread_str = ", ".join(str(card) for card in self.spread)
        logger.info("Generating a tarot card reading for %s for the following spread:\n\t%s\n",
                    self.command.subject, spread_str)
        tarot_reading_prompt = self.generate_tarot_reading_prompt()
        if self.command.show_prompt:
            logger.info("Prompt:\n%s\n", tarot_reading_prompt)
        card_reading = self.ask_openai_to_generate_card_reading(tarot_reading_prompt)
        card_reading.metadata.max_tokens = self.__config.openai.generate_reading.max_tokens
        logger.info("Response:\n%s", card_reading.response)
        self.ask_openai_to_summarize_card_reading(card_reading)
        return card_reading

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
        completion_kwargs = _make_openai_completion_request(self.__config.openai.generate_reading, prompt)
        completion, response = _execute_completion_request(completion_kwargs)
        command = self.command
        card_reading = CardReading(completion, self.spread, prompt, response, None, command.subject, command.teller)
        card_reading.metadata.max_tokens = self.__config.openai.generate_reading.max_tokens
        if 'temperature' in completion_kwargs:
            card_reading.metadata.temperature = completion_kwargs['temperature']
        if 'top_p' in completion_kwargs:
            card_reading.metadata.top_p = completion_kwargs['top_p']
        return card_reading

    def ask_openai_to_summarize_card_reading(self, card_reading):
        """Asks openai to interpret the tone of the tarot card reading it just generated and adds to the DTO."""
        prompt = f'Classify the sentiment of this tarot card reading: "{card_reading.response}"'
        completion_kwargs = _make_openai_completion_request(self.__config.openai.summarize_reading, prompt)
        summary_completion, summary_response = _execute_completion_request(completion_kwargs)
        logger.info("The tarot card reading sentiment:\n%s", summary_response)
        summary_metadata = Metadata(summary_completion)
        card_reading.summary = summary_response
        card_reading.metadata.response_ms += summary_metadata.response_ms
        card_reading.metadata.max_tokens += self.__config.openai.summarize_reading.max_tokens
        card_reading.metadata.total_tokens += summary_metadata.total_tokens
        card_reading.metadata.prompt_tokens += summary_metadata.prompt_tokens
        card_reading.metadata.completion_tokens += summary_metadata.completion_tokens
        return summary_response


def _make_openai_completion_request(config: Completion, prompt: str):
    """Builds the keyword arguments for an openai completion request for the associated configuration and prompt."""
    completion_kwargs = {
        'model': config.model,
        'max_tokens': config.max_tokens,
        'prompt': prompt
    }
    if config.n is not None:
        completion_kwargs['n'] = config.n
    if config.temperature is not None:
        completion_kwargs['temperature'] = config.temperature
    if config.top_p is not None:
        completion_kwargs['top_p'] = config.top_p
    return completion_kwargs


def _execute_completion_request(completion_kwargs):
    """Executes an openai completion request, returning a tuple of the Completion object and the response string."""
    completion = openai.Completion.create(**completion_kwargs)
    response = "\n".join(list(choice.text for choice in completion.choices)).strip()
    return completion, response


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
