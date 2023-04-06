#!/usr/bin/env python3

from test_with_config import TestWithConfig
from argparse import ArgumentError
from app import CommandParser
from tarot import TarotCard
import unittest


class TestCommandParser(TestWithConfig):

    def test_parse_command_line_args(self):
        # Given: some mocked up command line arguments
        parser = CommandParser(self.config, self.resolver)
        args = [
            '--card-count', '4',
            '--subject', 'nobody',
            '--teller', 'a mystic',
            '--show-prompt',
            '--show-diagnostics'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the command object
        self.assertEqual(4, command.card_count)
        self.assertEqual('nobody', command.subject)
        self.assertEqual('a mystic', command.teller)
        self.assertTrue(command.show_prompt)
        self.assertTrue(command.show_diagnostics)

    def test_parse_command_line_args_invalid_card_count(self):
        # Given: some mocked up command line arguments
        parser = CommandParser(self.config, self.resolver)
        args = ['--card-count', '42']

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to an illegal argument
        with self.assertRaises(ArgumentError) as arg_error:
            parser.parse_command_line_args(args)
        self.assertEqual("argument --card-count: invalid choice: 42 (choose from 1, 2, 3, 4, 5)", str(arg_error.exception))

    def test_parse_command_line_args_with_cards(self):
        # Given: some mocked up command line arguments with cards specified
        parser = CommandParser(self.config, self.resolver)
        args = [
            '--use-card-list',
            'The Magician',
            'The World',
            'seven of Wands'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the command object
        self.assertEqual('the seeker', command.subject)
        self.assertIsNone(command.teller)
        self.assertFalse(command.show_prompt)
        self.assertEqual([
            TarotCard.TheMagician,
            TarotCard.TheWorld,
            TarotCard.SevenOfWands
        ], command.given_cards)

    def test_parse_command_line_args_with_bad_card(self):
        # Given: some mocked up command line arguments with cards specified (including bogus)
        parser = CommandParser(self.config, self.resolver)
        args = [
            '--use-card-list',
            'MAGICIAN',
            'World',
            'FooOfBar'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to an unknown tarot card
        with self.assertRaises(ValueError) as val_error:
            parser.parse_command_line_args(args)
        self.assertEqual("Unknown card: FooOfBar", str(val_error.exception))

    def test_parse_command_line_args_with_dupe_card(self):
        # Given: some mocked up command line arguments with cards specified (including dupe)
        parser = CommandParser(self.config, self.resolver)
        args = [
            '--use-card-list',
            'TheMagician',
            'TheWorld',
            'KingOfPentacles',
            'KingOfDiscs'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to at least one duplicate tarot card
        with self.assertRaises(ValueError) as val_error:
            parser.parse_command_line_args(args)
        self.assertEqual("Duplicate card: King of Pentacles", str(val_error.exception))

    def test_parse_command_line_args_with_too_many_cards(self):
        # Given: some mocked up app config and command line arguments with cards specified
        conf = self.config
        conf.tarot.max_cards = 3
        parser = CommandParser(self.config, self.resolver)
        args = [
            '--use-card-list',
            'TheMagician',
            'TheWorld',
            'KingOfPentacles',
            'PageOfSwords'
        ]

        # When:  the command line arguments are parsed
        # Then:  an exception is raised due to more cards being specified than is allowed
        with self.assertRaises(ValueError) as val_error:
            parser.parse_command_line_args(args)
        self.assertEqual("Only [1-3] cards allowed in the tarot card spread", str(val_error.exception))


if __name__ == '__main__':
    unittest.main()
