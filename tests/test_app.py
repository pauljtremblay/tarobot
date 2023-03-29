#!/usr/bin/env python3

from app import App
import argparse
from tarot import TarotCard
import unittest


class TestApp(unittest.TestCase):

    def test_generate_tarot_reading_prompt(self):
        # Given: a mocked up subject, fortune-teller, and tarot spread
        app = App()
        app.subject = 'SomeGuy'
        app.teller = 'an optimist'
        app.spread = [TarotCard.TheFool, TarotCard.KingOfPentacles, TarotCard.TheTower]

        # When:  the fortune-telling prompt is generated
        actual = app.generate_tarot_reading_prompt()

        # Then:  the expected formatted prompt is returned
        self.assertEqual(actual, "Tarot card reading for SomeGuy with the cards The Fool, King of Pentacles, and The "
                                 "Tower in the style of an optimist")

    def test_draw_tarot_spread(self):
        # Given: a mocked up number of cards to draw
        app = App()
        app.card_count = 4

        # When:  the tarot card spread is drawn
        app.draw_tarot_spread()

        # Then:  the expected number of cards is drawn
        self.assertEqual(4, len(app.spread))

    def test_parse_command_line_args_happy_path(self):
        # Given: some mocked up command line arguments
        app = App()
        args = [
            '--card_count', '4',
            '--subject', 'nobody',
            '--teller', 'a mystic',
            '--show-prompt'
        ]

        # When:  the command line arguments are parsed
        app.parse_command_line_args(args)

        # Then:  the parsed arguments can be found in the app object
        self.assertEqual(4, app.card_count)
        self.assertEqual('nobody', app.subject)
        self.assertEqual('a mystic', app.teller)
        self.assertTrue(app.show_prompt)

    def test_parse_command_line_args_invalid_card_count(self):
        # Given: some mocked up command line arguments
        app = App()
        args = ['--card_count', '42']

        # When:  the command line arguments are parsed
        # Then:  an exception is raised
        with self.assertRaises(argparse.ArgumentError):
            app.parse_command_line_args(args)


if __name__ == '__main__':
    unittest.main()
