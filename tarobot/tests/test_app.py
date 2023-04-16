#!/usr/bin/env python3

"""Module containing all the core application's unit tests."""
from unittest.mock import patch

from openai import Completion

# pylint: disable=E0401
from base_test_with_config import BaseTestWithConfig
# pylint: enable=E0401
from tarobot.tarot import CardReading, TarotCard
from tarobot.app import App, CommandDto


# pylint: disable=C0115,C0116
class Choice:
    text: str


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

    @patch('tarobot.app.app.persist_card_reading')
    @patch('tarobot.app.app.openai.Completion.create')
    def test_interpret_tarot_spread(self, mock_openai_generate, mock_persist_reading):
        # Given: a mocked up command
        app = App(self.test_config)
        command = CommandDto()
        app.command = command
        command.show_prompt = True
        command.show_diagnostics = True
        command.persist_reading = True
        command.subject = "the seeker"
        command.teller = "Dr Seuss"
        # And:  a mocked up tarot spread
        spread = [TarotCard.TheMagician, TarotCard.TheTower]
        app.spread = spread
        # And:  a stubbed out response from openai
        completion = Completion(id='cmpl-444555', engine='generate', response_ms=1234)
        completion['model'] = 'scatgpt-4'
        completion['created'] = 1681571451
        completion['max_tokens'] = 2000
        completion['usage'] = {'prompt_tokens': 30, 'completion_tokens': 200, 'total_tokens': 230}
        completion['top_p'] = 0.1
        choice = Choice()
        choice.text = 'one fish two fish red fish dead fish'
        completion['choices'] = [choice]
        mock_openai_generate.return_value = completion

        # When:  the app interprets the tarot spread via openai
        app.interpret_tarot_spread()
        card_reading: CardReading
        (card_reading,) = mock_persist_reading.mock_calls[0][1]

        # Then:  the card reading contains the openai tarot/request inputs plus the response values
        self.assertEqual("cmpl-444555", card_reading.metadata.openai_id)
        self.assertEqual("scatgpt-4", card_reading.metadata.model)
        self.assertEqual(1681571451, card_reading.metadata.created_ts)
        self.assertEqual(1234, card_reading.metadata.response_ms)
        self.assertEqual(2000, card_reading.metadata.max_tokens)
        self.assertEqual(30, card_reading.metadata.prompt_tokens)
        self.assertEqual(200, card_reading.metadata.completion_tokens)
        self.assertEqual(230, card_reading.metadata.total_tokens)
        self.assertIsNone(card_reading.metadata.temperature)
        self.assertEqual(0.1, card_reading.metadata.top_p)
        self.assertEqual([TarotCard.TheMagician, TarotCard.TheTower], card_reading.spread)
        self.assertEqual("Tarot card reading for the seeker with the cards The Magician, and The Tower in the style of "
                         "Dr Seuss", card_reading.prompt)
        self.assertEqual("one fish two fish red fish dead fish", card_reading.response)
        self.assertEqual("the seeker", card_reading.subject)
        self.assertEqual("Dr Seuss", card_reading.teller)

    @patch('tarobot.app.app.App.interpret_tarot_spread')
    @patch('tarobot.app.app.App.create_tarot_spread')
    @patch('tarobot.app.command_parser.CommandParser.parse_command_line_args')
    def test_main(self, mock_parse_cmd_args, mock_create_spread, mock_interpret_spread):
        # Given: a mocked up user request
        app = App()
        command = CommandDto()
        mock_parse_cmd_args.return_value = command

        # When:  the main app is run
        app.main()

        # Then:  the parsed config is stored
        self.assertEqual(command, app.command)
        # And:   the expected helper methods are called
        mock_create_spread
        self.assertTrue(mock_create_spread.called)
        self.assertTrue(mock_interpret_spread.called)
# pylint: enable=C0115,C0116
