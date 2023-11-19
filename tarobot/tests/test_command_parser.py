#!/usr/bin/env python3

"""Module containing unit tests around parsing user input from the command line."""

from argparse import ArgumentError

# pylint: disable=E0401
from base_test_with_config import BaseTestWithConfig
# pylint: enable=E0401
from tarobot.tarot import TarotCard
from tarobot.app import CommandParser


# pylint: disable=C0115,C0116
class TestCommandParser(BaseTestWithConfig):

    def test_parse_command_line_args(self):
        # Given: some mocked up command line arguments
        parser = CommandParser(self.test_config)
        args = [
            '--show-prompt',
            '--show-diagnostics',
            '--persist-reading',
            'card-list',
            '--card-count', '4',
            '--seeker', 'nobody',
            '--teller', 'a mystic'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the command object
        self.assertEqual(4, command.card_count)
        self.assertEqual('nobody', command.spread_parameters['seeker'])
        self.assertEqual('a mystic', command.spread_parameters['teller'])
        self.assertTrue(command.show_prompt)
        self.assertTrue(command.show_diagnostics)
        self.assertTrue(command.persist_reading)

    def test_parse_command_line_args_invalid_card_count(self):
        # Given: some mocked up command line arguments
        parser = CommandParser(self.test_config)
        args = [
            'card-list',
            '--card-count', '42'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to an illegal argument
        with self.assertRaises(ArgumentError) as arg_error:
            parser.parse_command_line_args(args)
        self.assertEqual("argument --card-count: invalid choice: 42 (choose from 1, 2, 3, 4, 5)",
                         str(arg_error.exception))

    def test_parse_command_line_args_invalid_mutual_exclusive_config(self):
        # Given: an illegal combo of card count and specified cards
        parser = CommandParser(self.test_config)
        args = [
            'card-list',
            '--card-count', '4',
            '--card', 'The Magician', 'Nine of Cups'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to an illegal combination of arguments
        with self.assertRaises(ArgumentError) as arg_error:
            parser.parse_command_line_args(args)
        self.assertEqual("argument --card: not allowed with argument --card-count",
                         str(arg_error.exception))

    def test_parse_command_line_args_with_cards(self):
        # Given: some mocked up command line arguments with cards specified
        parser = CommandParser(self.test_config)
        args = [
            'card-list',
            '--card', 'The Magician', 'The World', 'seven of Wands'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the command object
        self.assertEqual('the seeker', command.spread_parameters['seeker'])
        self.assertEqual('a mystic', command.spread_parameters['teller'])
        self.assertFalse(command.show_prompt)
        self.assertEqual([
            TarotCard.TheMagician,
            TarotCard.TheWorld,
            TarotCard.SevenOfWands
        ], command.given_cards)

    def test_parse_command_line_args_with_bad_card(self):
        # Given: some mocked up command line arguments with cards specified (including bogus)
        parser = CommandParser(self.test_config)
        args = [
            'card-list',
            '--card', 'MAGICIAN', 'World', 'FooOfBar', 'card-list'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to an unknown tarot card
        with self.assertRaises(ValueError) as val_error:
            parser.parse_command_line_args(args)
        self.assertEqual("Unknown card: FooOfBar", str(val_error.exception))

    def test_parse_command_line_args_with_dupe_card(self):
        # Given: some mocked up command line arguments with cards specified (including dupe)
        parser = CommandParser(self.test_config)
        args = [
            'card-list',
            '--card', 'TheMagician', 'TheWorld', 'KingOfPentacles', 'KingOfDiscs'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to at least one duplicate tarot card
        with self.assertRaises(ValueError) as val_error:
            parser.parse_command_line_args(args)
        self.assertEqual("Duplicate card: King of Pentacles", str(val_error.exception))

    def test_parse_command_line_args_with_too_many_cards(self):
        # Given: some mocked up app config and command line arguments with cards specified
        conf = self.test_config
        conf.tarot.max_cards = 3
        parser = CommandParser(self.test_config)
        args = [
            'card-list',
            '--card', 'TheMagician', 'TheWorld', 'KingOfPentacles', 'PageOfSwords'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to more cards being specified than is allowed
        with self.assertRaises(ValueError) as val_error:
            parser.parse_command_line_args(args)
        self.assertEqual("Only [1-3] cards allowed in the tarot card spread", str(val_error.exception))
# pylint: enable=C0115,C0116
