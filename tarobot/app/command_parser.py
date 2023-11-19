#!/usr/bin/env python3

"""Utility that parses the user input into commands and options for tarobot."""

from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from . config import Config, Tarot as TarotConfig
from .. tarot import resolver, spread_builder, SpreadTemplate, SpreadType, TarotCard, TarotDeck


@dataclass
class CommandDto:
    """Data class used for storing the commands given to the application from the user."""
    show_prompt: bool = False
    show_diagnostics: bool = False
    persist_reading: bool = False
    spread_type: SpreadType = SpreadType.CARD_LIST
    spread_parameters: Optional[Dict[str, str]] = None
    given_cards: List[TarotCard] = None
    card_count: int = 3


class CommandParser:
    """This class processes input from command line arguments for later execution."""

    def __init__(self, config: Config):
        self.parser: ArgumentParser
        self.command: CommandDto
        self.parsed_args = None
        self.config = config
        self.parser = _build_parser(config)

    def parse_command_line_args(self, command_line_args: List[str]):
        """Parses the given command line args into a command dto."""
        parsed_command = CommandDto()
        self.parsed_args = self.parser.parse_args(command_line_args)
        parsed_command.show_prompt = self.parsed_args.show_prompt
        parsed_command.show_diagnostics = self.parsed_args.show_diagnostics
        parsed_command.persist_reading = self.parsed_args.persist_reading
        parsed_command.spread_type = SpreadType(self.parsed_args.spread_type)
        parsed_command.card_count = self.parsed_args.card_count
        spread_template: SpreadTemplate = [template
                                           for template in spread_builder.spread_type_to_template.values()
                                           if template.type == parsed_command.spread_type][0]
        if self.parsed_args.card is not None:
            parsed_command.given_cards = self.parse_given_tarot_cards(spread_template)
        parsed_command.spread_parameters = {}
        if spread_template.required_parameters is not None:
            for parameter in spread_template.required_parameters.keys():
                parsed_command.spread_parameters[parameter] = getattr(self.parsed_args, parameter)
        return parsed_command

    def parse_given_tarot_cards(self, spread_template: SpreadTemplate):
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
        min_cards, max_cards = _get_min_max_card_count_for_template(spread_template, self.config.tarot)
        if len(parsed_cards) not in range(min_cards, max_cards + 1):
            raise ValueError(f"Only [{min_cards}-{max_cards}] cards allowed in the tarot card spread")
        return parsed_cards

    def print_parse_error_and_exit(self, arg_error):
        """Used to format the error raised while parsing user input, and then exits with a non-zero exit code.

        Used so fatal argparse errors can be unit tested."""
        self.parser.error(arg_error)


def _build_parser(config: Config) -> ArgumentParser:
    """The command line argument parser config for the tarobot application."""
    tarot = config.tarot
    parser: ArgumentParser = ArgumentParser(
        prog=config.app_name.lower(),
        description='Tarot deck cartomancy application',
        exit_on_error=False)
    parser.add_argument(
        '--show-prompt',
        help='displays the generated prompt ahead of the response',
        action='store_true')
    parser.add_argument(
        '--show-diagnostics',
        help='displays diagnostic output from the completion response returned from openai',
        action='store_true')
    parser.add_argument(
        '--persist-reading',
        help='inserts a record of the tarot card reading (inputs, prompt, result, metadata) in the database',
        action='store_true')
    spread_type_subparsers = parser.add_subparsers(
        title='spread-type',
        dest='spread_type',
        help='spread-type help',
        required=True)
    for spread_template in spread_builder.spread_type_to_template.values():
        _build_spread_type_parser(spread_type_subparsers, spread_template, tarot)
    return parser


def _build_spread_type_parser(spread_type_subparsers, template: SpreadTemplate, tarot: TarotConfig) -> None:
    """Constructs a subparser for the given tarot pread template configuration."""
    spread_type_parser = spread_type_subparsers.add_parser(
        template.type,
        exit_on_error=False,
        help=template.description)
    _build_card_count_or_card_list_parser(spread_type_parser, template, tarot)
    if template.required_parameters is not None:
        for (param_name, parameter) in template.required_parameters.items():
            description = parameter.description
            if parameter.default_value is not None:
                description += f"\n\tdefault: \"{parameter.default_value}\""
            spread_type_parser.add_argument(
                f"--{param_name}",
                help=description,
                default=parameter.default_value,
                required=parameter.default_value is None)


def _build_card_count_or_card_list_parser(spread_type_parser, template: SpreadTemplate, tarot: TarotConfig) -> None:
    """Constructs a mutually exclusive parser that either specifies a card count or a list of specified cards."""
    card_count_or_list_mutex_args = spread_type_parser.add_mutually_exclusive_group()
    min_cards, max_cards = _get_min_max_card_count_for_template(template, tarot)
    card_count_or_list_mutex_args.add_argument(
        '--card-count',
        help=f"number of tarot cards to draw in the spread [{min_cards}-{max_cards}]"
             f"\n\tdefault: {tarot.default_cards} card spread",
        type=int,
        choices=range(min_cards, max_cards + 1),
        default=tarot.default_cards)
    card_count_or_list_mutex_args.add_argument(
        '--card',
        help='takes specific card[s] from the user instead of a random draw from the deck',
        type=str,
        nargs='+')


def _get_min_max_card_count_for_template(template: SpreadTemplate, tarot: TarotConfig) -> Tuple[int, int]:
    if template.required_card_count is None:
        min_cards = tarot.min_cards
        max_cards = tarot.max_cards
    else:
        min_cards = template.required_card_count
        max_cards = template.required_card_count
    return min_cards, max_cards
