#!/usr/bin/env python3

"""Module containing all the core application's unit tests."""

import unittest

# pylint: disable=E0401
from base_test_with_config import BaseTestWithConfig
# pylint: enable=E0401
from tarobot.tarot import TarotCard
from tarobot.app import App, CommandDto


# pylint: disable=C0115,C0116
class TestApp(BaseTestWithConfig):

    def test_create_tarot_spread_by_deck(self):
        # Given: a mocked up number of cards to draw
        app = App(self.test_config)
        command = CommandDto()
        command.card_count = 4
        app.command = command

        # When:  the tarot card spread is created
        app.create_tarot_spread()

        # Then:  the expected number of cards is drawn
        self.assertEqual(4, len(app.spread))

    def test_create_tarot_spread_by_given_cards(self):
        # Given: a mocked up request with specified cards
        app = App(self.test_config)
        command = CommandDto()
        command.given_cards = [
            TarotCard.TheMagician,
            TarotCard.SixOfWands,
            TarotCard.TheTower
        ]
        app.command = command

        # When:  the tarot card spread is created
        app.create_tarot_spread()

        # Then:  the expected spread is found
        self.assertEqual(3, len(app.spread))
        self.assertEqual([
            TarotCard.TheMagician,
            TarotCard.SixOfWands,
            TarotCard.TheTower
        ], app.spread)

    def test_generate_tarot_reading_prompt(self):
        # Given: a subject
        app = App(self.test_config)
        command = CommandDto()
        app.command = command
        command.subject = 'The Seeker'
        # And:   a fortune teller
        command.teller = 'Hulk Hogan'
        # And:   a tarot card spread
        app.spread = [
            TarotCard.TheTower,
            TarotCard.Death,
            TarotCard.SevenOfSwords
        ]

        # When:  the prompt is generated
        prompt = app.generate_tarot_reading_prompt()

        # Then:  the exact expected prompt is generated
        self.assertEqual(prompt, "Tarot card reading for The Seeker with the cards The Tower, Death, and Seven of "
                                 "Swords in the style of Hulk Hogan")
# pylint: enable=C0115,C0116


if __name__ == '__main__':
    unittest.main()