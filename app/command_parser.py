#!/usr/bin/env python3
from argparse import ArgumentParser
from dataclasses import dataclass
from tarot import TarotCard, TarotDeck
from typing import List


@dataclass
class CommandDto:
    """Data class used for storing the commands given to the application from the user."""
    subject: str = None
    teller: str = None
    show_prompt: bool = False
    given_cards: List[TarotCard] = None
    card_count: int = 3


class CommandParser:
    """This class processes input from command line arguments for later execution."""

    def __init__(self):
        self.parser: ArgumentParser
        self.command: CommandDto
        self.parsed_args = None
        self.__build_parser()

    def __build_parser(self):
        """The command line argument parser config for the tarobot application."""
        self.parser = ArgumentParser(
            prog='tarobot',
            description='Tarot deck cartomancy application',
            exit_on_error=False)
        self.parser.add_argument(
            '--card-count',
            help='number of tarot cards to draw in the spread [1-5]\n\tdefault: 3 card spread',
            type=int,
            choices=range(1, 5 + 1),
            default=3)
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

    def parse_command_line_args(self, command_line_args):
        """Parses the given command line args into a command dto."""
        parsed_command = CommandDto()
        self.parsed_args = self.parser.parse_args(command_line_args)
        parsed_command.card_count = self.parsed_args.card_count
        parsed_command.subject = self.parsed_args.subject
        parsed_command.show_prompt = self.parsed_args.show_prompt
        if self.parsed_args.teller is not None:
            parsed_command.teller = self.parsed_args.teller
        if self.parsed_args.use_card_list is not None:
            parsed_command.given_cards = self.parse_given_tarot_cards()
            if len(parsed_command.given_cards) not in range(1, 5 + 1):
                raise ValueError("Only [1-5] cards allowed in the tarot card spread")
        return parsed_command

    def parse_given_tarot_cards(self):
        """Helper method for validating and parsing the given tarot cards."""
        # TODO normalize names (coins, disks -> pentacles, pope -> hierophant, etc.)
        # ensure the cards are valid tarot cards
        try:
            parsed_cards = [TarotCard[card_name] for card_name in self.parsed_args.use_card_list]
        except KeyError as bad_card:
            raise ValueError("Unknown card: {}".format(bad_card))
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
