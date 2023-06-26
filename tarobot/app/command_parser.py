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
    situation: str = None
    obstacle: str = None


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
        spread_type_subparsers = self.parser.add_subparsers(
            title='spread-type',
            dest='spread_type',
            help='spread-type help',
            required=True)
        card_list_parser = spread_type_subparsers.add_parser(
            'card-list',
            exit_on_error=False,
            help='Perform a tarot card spread on a list of cards, with a fortune teller and seeker')
        card_count_or_list_mutex_args = card_list_parser.add_mutually_exclusive_group()
        card_count_or_list_mutex_args.add_argument(
            '--card-count',
            help=f"number of tarot cards to draw in the spread [{tarot.min_cards}-{tarot.max_cards}]"
                 f"\n\tdefault: {tarot.default_cards} card spread",
            type=int,
            choices=range(tarot.min_cards, tarot.max_cards + 1),
            default=tarot.default_cards)
        card_count_or_list_mutex_args.add_argument(
            '--card',
            help='takes specific card[s] from the user instead of a random draw from the deck',
            type=str,
            nargs='+')
        card_list_parser.add_argument(
            '--seeker',
            help='tarot reading recipient\n\tdefault: "the seeker"',
            type=str,
            default='the seeker')
        card_list_parser.add_argument(
            '--teller',
            help='person performing tarot reading\n\tdefault: "a mystic"',
            type=str,
            default='a mystic')
        spread_type_subparsers.add_parser(
            'one-card',
            exit_on_error=False,
            help='Perform a simple one card tarot card spread')
        spread_type_subparsers.add_parser(
            'past-present-future',
            exit_on_error=False,
            help='Perform a three card tarot card spread: C1 = past, C2 = present, C3 = future')
        spread_type_subparsers.add_parser(
            'seeker-subject-relationship',
            exit_on_error=False,
            help='Perform a three card tarot card spread: C1 = seeker, C2 = subject, C3 = relationship')
        situation_obstacle_advice_parser = spread_type_subparsers.add_parser(
            'situation-obstacle-advice',
            exit_on_error=False,
            help='Perform a three card tarot card spread: C1 = situation, C2 = obstacle, C3 = advice')
        situation_obstacle_advice_parser.add_argument(
            '--situation',
            help='situation being explored by tarot card reading',
            type=str,
            required=True)
        situation_obstacle_advice_parser.add_argument(
            '--obstacle',
            help='obstacle in the situation being addressed by the tarot card reading',
            type=str,
            required=True)

    def parse_command_line_args(self, command_line_args: List[str]):
        """Parses the given command line args into a command dto."""
        parsed_command = CommandDto()
        self.parsed_args = self.parser.parse_args(command_line_args)
        parsed_command.show_prompt = self.parsed_args.show_prompt
        parsed_command.show_diagnostics = self.parsed_args.show_diagnostics
        parsed_command.persist_reading = self.parsed_args.persist_reading
        parsed_command.spread_type = SpreadType(self.parsed_args.spread_type)
        # handle spread-specific parameters conditionally
        match parsed_command.spread_type:
            case SpreadType.CARD_LIST:
                self._parse_card_list_subcommand(parsed_command)

            case SpreadType.SITUATION_OBSTACLE_ADVICE:
                parsed_command.situation = self.parsed_args.situation
                parsed_command.obstacle = self.parsed_args.obstacle
        return parsed_command

    def _parse_card_list_subcommand(self, parsed_command):
        """Helper method that parses the card-list subcommand, tarot card spread."""
        parsed_command.seeker = self.parsed_args.seeker
        parsed_command.teller = self.parsed_args.teller
        parsed_command.card_count = self.parsed_args.card_count
        if self.parsed_args.card is not None:
            parsed_command.given_cards = self.parse_given_tarot_cards()
            tarot = self.__config.tarot
            if len(parsed_command.given_cards) not in range(tarot.min_cards, tarot.max_cards + 1):
                raise ValueError(f"Only [{tarot.min_cards}-{tarot.max_cards}] cards allowed in the tarot card spread")

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
