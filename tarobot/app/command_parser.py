#!/usr/bin/env python3

"""Utility that parses the user input into commands and options for tarobot."""

from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List

from . config import Config
from .. tarot import resolver, SpreadType, TarotCard, TarotDeck


@dataclass
class CommandDto:
    """Data class used for storing the commands given to the application from the user."""
    show_prompt: bool = False
    show_diagnostics: bool = False
    persist_reading: bool = False
    spread_type: SpreadType = SpreadType.CARD_LIST
    given_cards: List[TarotCard] = None
    card_count: int = 3
    seeker: str = None
    teller: str = None


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
        mutually_exclusive_args = self.parser.add_mutually_exclusive_group()
        mutually_exclusive_args.add_argument(
            '--card-count',
            help=f"number of tarot cards to draw in the spread [{tarot.min_cards}-{tarot.max_cards}]"
                 f"\n\tdefault: {tarot.default_cards} card spread",
            type=int,
            choices=range(tarot.min_cards, tarot.max_cards + 1),
            default=tarot.default_cards)
        mutually_exclusive_args.add_argument(
            '--card',
            help='takes specific card[s] from the user instead of a random draw from the deck',
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
        self.parser.add_argument(
            '--seeker',
            help='the name of the person receiving the tarot card reading\n\tdefault: "the seeker"',
            type=str,
            default='the seeker')
        self.parser.add_argument(
            '--teller',
            help='the "person" conducting the tarot card reading\n\tdefault: "a mystic"',
            type=str,
            default='a mystic')


    def parse_command_line_args(self, command_line_args: List[str]):
        """Parses the given command line args into a command dto."""
        parsed_command = CommandDto()
        self.parsed_args = self.parser.parse_args(command_line_args)
        parsed_command.card_count = self.parsed_args.card_count
        parsed_command.show_prompt = self.parsed_args.show_prompt
        parsed_command.show_diagnostics = self.parsed_args.show_diagnostics
        parsed_command.persist_reading = self.parsed_args.persist_reading
        if self.parsed_args.seeker is not None:
            parsed_command.seeker = self.parsed_args.seeker
        if self.parsed_args.teller is not None:
            parsed_command.teller = self.parsed_args.teller
        if self.parsed_args.card is not None:
            parsed_command.given_cards = self.parse_given_tarot_cards()
            tarot = self.__config.tarot
            if len(parsed_command.given_cards) not in range(tarot.min_cards, tarot.max_cards + 1):
                raise ValueError(f"Only [{tarot.min_cards}-{tarot.max_cards}] cards allowed in the tarot card spread")
        return parsed_command

    def parse_given_tarot_cards(self):
        """Helper method for validating and parsing the given tarot cards."""
        # ensure the cards are valid tarot cards
        parsed_cards = []
        for given_card_name in self.parsed_args.card:
            tarot_card = resolver.get_optional_card_by_alias(given_card_name)
            if tarot_card is None:
                raise ValueError(f"Unknown card: {given_card_name}")
            parsed_cards.append(tarot_card)
        # ensure a given card isn't used more than once
        tarot_deck = TarotDeck()
        for card in parsed_cards:
            try:
                tarot_deck.cards.remove(card)
            except ValueError as cause:
                raise ValueError(f"Duplicate card: {card}") from cause
        return parsed_cards

    def print_parse_error_and_exit(self, arg_error):
        """Used to format the error raised while parsing user input, and then exits with a non-zero exit code.

        Used so fatal argparse errors can be unit tested."""
        self.parser.error(arg_error)
