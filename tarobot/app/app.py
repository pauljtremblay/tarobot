#!/usr/bin/env python3

"""This module contains tarobot's core application logic."""

from argparse import ArgumentError
import logging
import sys
from typing import Dict, Optional, Tuple

from openai import OpenAI

from .. db import session_factory, CardReadingEntity
from .. tarot import TarotDeck, CardReading, Spread, spread_builder
from . command_parser import CommandDto, CommandParser
from . config import CONFIG, Config


logger = logging.getLogger(__name__)


STOP_SEQUENCE = "END-OF-TRANSMISSION"


class App:
    """This class processes input from command line arguments and executes the request."""

    def __init__(self, config_opt: Optional[Config] = None, openai_client: OpenAI = None):
        # load app config
        if config_opt is not None:
            self.__config = config_opt
        else:
            self.__config = CONFIG
        if openai_client is not None:
            self.openai_client = openai_client
        else:
            self.openai_client = OpenAI(api_key=self.__config.openai.api_key)
        self.parser = CommandParser(self.__config)
        self.command: Optional[CommandDto] = None
        self.spread: Optional[Spread] = None

    def main(self) -> None:
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

    def create_tarot_spread(self) -> None:
        """Creates a tarot spread from either the given cards or a locally created tarot card deck."""
        if self.command.given_cards is not None:
            tarot_cards = self.command.given_cards
        else:
            deck = TarotDeck()
            tarot_cards = deck.draw(self.command.card_count)
        self.spread = spread_builder.build(self.command.spread_type, tarot_cards, self.command.spread_parameters)

    def interpret_tarot_spread(self) -> CardReading:
        """Generates a tarot card reading for the given spread and logs the response."""
        card_list_str = ", ".join(str(card) for card in self.spread.tarot_cards)
        logger.info("Generating a %s tarot card reading for the following cards:\n\t%s\n",
                    str(self.spread.spread_type), card_list_str)
        if self.command.show_prompt:
            logger.info("Prompt:\n%s\n", self.spread.prompt)
        card_reading = self.ask_openai_to_generate_card_reading(self.spread.prompt)
        card_reading.metadata.max_tokens = self.spread.chat_completion_config.max_tokens
        logger.info("Response:\n%s", card_reading.response)
        return card_reading

    def ask_openai_to_generate_card_reading(self, prompt: str) -> CardReading:
        """Displays the prompt to and associated response from openai."""
        completion_kwargs = self._construct_openai_chat_completion_request()
        completion, response = _execute_chat_completion_request(self.openai_client, completion_kwargs)
        command = self.command
        card_reading = CardReading(completion, self.spread.tarot_cards, prompt, response, command.spread_parameters)
        card_reading.metadata.max_tokens = self.spread.chat_completion_config.max_tokens
        if 'temperature' in completion_kwargs:
            card_reading.metadata.temperature = completion_kwargs['temperature']
        if 'top_p' in completion_kwargs:
            card_reading.metadata.top_p = completion_kwargs['top_p']
        return card_reading

    def _construct_openai_chat_completion_request(self) -> Dict[str, any]:
        """Builds the keyword arguments for an openai chat completion request for the spread."""
        completion_config = self.spread.chat_completion_config
        completion_kwargs = {
            'model': completion_config.model,
            'max_tokens': completion_config.max_tokens,
            'messages': [
                {'role': 'assistant', 'content': "you are a helpful assistant."},
                {'role': 'user', 'content': f"{self.spread.prompt}\n{STOP_SEQUENCE}"}
            ]
            # 'prompt': self.spread.prompt
        }
        if completion_config.n is not None:
            completion_kwargs['n'] = completion_config.n
        if completion_config.temperature is not None:
            completion_kwargs['temperature'] = completion_config.temperature
        if completion_config.top_p is not None:
            completion_kwargs['top_p'] = completion_config.top_p
        return completion_kwargs


def _execute_chat_completion_request(openai_client: OpenAI, chat_completion_kwargs) -> Tuple[any, str]:
    """Executes an openai completion request, returning a tuple of the Completion object and the response string."""
    # tell the api this conversation is over
    chat_completion_kwargs['stop'] = STOP_SEQUENCE
    chat_completion = openai_client.chat.completions.create(**chat_completion_kwargs)
    response = "\n".join([choice.message.content.strip()
                          for choice in chat_completion.choices])
    return chat_completion, response


def persist_card_reading(card_reading_dto: CardReading) -> None:
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
