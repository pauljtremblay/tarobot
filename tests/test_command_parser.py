#!/usr/bin/env python3

from app import CommandParser
from tarot import TarotCard
import unittest


class TestCommandParser(unittest.TestCase):

    def test_parse_command_line_args(self):
        # Given: some mocked up command line arguments
        parser = CommandParser()
        args = [
            '--card-count', '4',
            '--subject', 'nobody',
            '--teller', 'a mystic',
            '--show-prompt'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the app object
        self.assertEqual(4, command.card_count)
        self.assertEqual('nobody', command.subject)
        self.assertEqual('a mystic', command.teller)
        self.assertTrue(command.show_prompt)

    def test_parse_command_line_args_invalid_card_count(self):
        # Given: some mocked up command line arguments
        parser = CommandParser()
        args = ['--card-count', '42']

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  nothing is returned as the command is invalid
        self.assertIsNone(command)

    def test_parse_command_line_args_with_cards(self):
        # Given: some mocked up command line arguments with cards specified
        parser = CommandParser()
        args = [
            '--use-card-list',
            'TheMagician',
            'TheWorld',
            'SevenOfWands'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the app object
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
        parser = CommandParser()
        args = [
            '--use-card-list',
            'TheMagician',
            'TheWorld',
            'FooOfBar'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the command is recognized as invalid
        self.assertIsNone(command)

    def test_parse_command_line_args_with_dupe_card(self):
        # Given: some mocked up command line arguments with cards specified (including dupe)
        parser = CommandParser()
        args = [
            '--use-card-list',
            'TheMagician',
            'TheWorld',
            'KingOfPentacles',
            'KingOfPentacles'
        ]

        # When:  the command line arguments are parsed
        command = parser.parse_command_line_args(args)

        # Then:  the command is recognized as invalid
        self.assertIsNone(command)


if __name__ == '__main__':
    unittest.main()
