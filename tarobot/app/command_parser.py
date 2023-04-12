#!/usr/bin/env python3

from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List

from . config import Config
from tarobot.tarot import resolver, TarotCard, TarotDeck


@dataclass
class CommandDto:
    """Data class used for storing the commands given to the application from the user."""
    subject: str = None
    teller: str = None
    show_prompt: bool = False
    show_diagnostics: bool = False
    persist_reading: bool = False
    given_cards: List[TarotCard] = None
    card_count: int = 3


class CommandParser:
    """This class processes input from command line arguments for later execution."""

    def __init__(self, config: Config):
        self.parser: ArgumentParser
        self.command: CommandDto
        self.parsed_args = None
        self.__config = config
        self.__build_parser(config)

    def __build_parser(self, config: Config):
        """The command line argument parser config for the tarobot application."""
        tarot = self.__config.tarot
        self.parser = ArgumentParser(
            prog=config.app_name.lower(),
            description='Tarot deck cartomancy application',
            exit_on_error=False)
        self.parser.add_argument(
            '--card-count',
            help="number of tarot cards to draw in the spread [{}-{}]\n\tdefault: {} card spread".format(
                tarot.min_cards, tarot.max_cards, tarot.default_cards),
            type=int,
            choices=range(tarot.min_cards, tarot.max_cards + 1),
            default=tarot.default_cards)
        self.parser.add_argument(
            '--subject',
            help='the name of the person receiving the tarot card reading\n\tdefault: "the seeker"',
            type=str,
            default='the seeker')
        self.parser.add_argument(
            '--teller',
            help='the "person" conducting the tarot card reading\n\t(optional)',
            type=str)
        self.parser.add_argument(
            '--use-card-list',
            help='takes specific cards from the user instead of a random draw from the deck',
            type=str,
            nargs='+')
        self.parser.add_argument(
            '--show-prompt',
            help='displays the generated prompt ahead of the response',
            action='store_true')
        self.parser.add_argument(
            '--show-diagnostics',
            help='displays diagnostic output from the completion response returned from openai',
            action='store_true')
        self.parser.add_argument(
            '--persist-reading',
            help='inserts a record of the tarot card reading (inputs, prompt, result, metadata) in the database',
            action='store_true')

    def parse_command_line_args(self, command_line_args: List[str]):
        """Parses the given command line args into a command dto."""
        parsed_command = CommandDto()
        self.parsed_args = self.parser.parse_args(command_line_args)
        parsed_command.card_count = self.parsed_args.card_count
        parsed_command.subject = self.parsed_args.subject
        parsed_command.show_prompt = self.parsed_args.show_prompt
        parsed_command.show_diagnostics = self.parsed_args.show_diagnostics
        parsed_command.persist_reading = self.parsed_args.persist_reading
        if self.parsed_args.teller is not None:
            parsed_command.teller = self.parsed_args.teller
        if self.parsed_args.use_card_list is not None:
            parsed_command.given_cards = self.parse_given_tarot_cards()
            tarot = self.__config.tarot
            if len(parsed_command.given_cards) not in range(tarot.min_cards, tarot.max_cards + 1):
                raise ValueError("Only [{}-{}] cards allowed in the tarot card spread".format(
                    tarot.min_cards, tarot.max_cards))
        return parsed_command

    def parse_given_tarot_cards(self):
        """Helper method for validating and parsing the given tarot cards."""
        # ensure the cards are valid tarot cards
        parsed_cards = []
        for given_card_name in self.parsed_args.use_card_list:
            tarot_card = resolver.get_optional_card_by_alias(given_card_name)
            if tarot_card is None:
                raise ValueError("Unknown card: {}".format(given_card_name))
            else:
                parsed_cards.append(tarot_card)
        # ensure a given card isn't used more than once
        tarot_deck = TarotDeck()
        for card in parsed_cards:
            try:
                tarot_deck.cards.remove(card)
            except ValueError:
                raise ValueError("Duplicate card: {}".format(card))
        return parsed_cards

    def print_parse_error_and_exit(self, arg_error):
        self.parser.error(arg_error)
