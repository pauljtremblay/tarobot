#!/usr/bin/env python3

"""Module containing all the core application's unit tests."""
from unittest.mock import patch

from openai import Completion

# pylint: disable=E0401
from base_test_with_config import BaseTestWithConfig
# pylint: enable=E0401
from tarobot.tarot import CardReading, Spread, SpreadType, TarotCard
from tarobot.app import App, CommandDto


# pylint: disable=C0115,C0116,R0903
class Choice:
    text: str


class TestApp(BaseTestWithConfig):

    def test_create_tarot_spread_by_deck(self):
        # Given: a mocked up number of cards to draw
        app = App(self.test_config)
        command = CommandDto(spread_type=SpreadType.CARD_LIST,
                             seeker='the seeker',
                             teller='a mystic')
        command.card_count = 4
        app.command = command

        # When:  the tarot card spread is created
        app.create_tarot_spread()

        # Then:  the expected number of cards is drawn
        self.assertEqual(4, len(app.spread.tarot_cards))

    def test_create_tarot_spread_by_given_cards(self):
        # Given: a mocked up request with specified cards
        app = App(self.test_config)
        app.command = CommandDto(spread_type=SpreadType.CARD_LIST,
                                 seeker='the seeker',
                                 teller='a mystic',
                                 given_cards=[TarotCard.TheMagician, TarotCard.SixOfWands, TarotCard.TheTower])

        # When:  the tarot card spread is created
        app.create_tarot_spread()

        # Then:  the expected spread is found
        self.assertEqual(SpreadType.CARD_LIST, app.spread.spread_type)
        self.assertEqual(3, len(app.spread.tarot_cards))
        self.assertEqual([TarotCard.TheMagician, TarotCard.SixOfWands,TarotCard.TheTower], app.spread.tarot_cards)

    @patch('tarobot.app.app.openai.Completion.create')
    def test_interpret_tarot_spread(self, mock_openai_generate):
        # Given: a mocked up command
        app = App(self.test_config)
        command = CommandDto()
        app.command = command
        command.show_prompt = True
        command.show_diagnostics = True
        command.persist_reading = True
        command.seeker = "the seeker"
        command.teller = "Dr Seuss"
        # And:  a mocked up tarot spread
        tarot_cards = [TarotCard.TheMagician, TarotCard.TheTower]
        app.spread = Spread(spread_type=app.command.spread_type,
                            tarot_cards=tarot_cards,
                            parameters={'seeker': 'the seeker', 'teller': 'Dr Seuss'},
                            prompt=('Tarot card reading for the seeker '
                                    'with the cards The Magician, The Tower '
                                    'in the style of Dr Seuss.'))
        # And:  stubbed out responses from openai
        reading_completion = Completion(id='cmpl-444555', engine='generate', response_ms=1234)
        reading_completion['model'] = 'scatgpt-4'
        reading_completion['created'] = 1681571451
        reading_completion['max_tokens'] = 2000
        reading_completion['usage'] = {'prompt_tokens': 30, 'completion_tokens': 200, 'total_tokens': 230}
        reading_completion['top_p'] = 0.1
        reading_choice = Choice()
        reading_choice.text = 'one fish two fish red fish dead fish'
        reading_completion['choices'] = [reading_choice]
        summary_completion = Completion(id='cmpl-555666', engine='generate', response_ms=123)
        summary_completion['model'] = 'scatgpt-4'
        summary_completion['created'] = 1681571455
        summary_completion['max_tokens'] = 2000
        summary_completion['usage'] = {'prompt_tokens': 50, 'completion_tokens': 5, 'total_tokens': 55}
        summary_completion['top_p'] = 0.1
        summary_choice = Choice()
        summary_choice.text = 'Mixed'
        summary_completion['choices'] = [summary_choice]
        mock_openai_generate.side_effect = [reading_completion, summary_completion]

        # When:  the app interprets the tarot spread via openai
        card_reading: CardReading = app.interpret_tarot_spread()

        # Then:  the card reading contains the openai tarot/request inputs plus the response values
        self.assertEqual("cmpl-444555", card_reading.metadata.openai_id)
        self.assertEqual("scatgpt-4", card_reading.metadata.model)
        self.assertEqual(1681571451, card_reading.metadata.created_ts)
        self.assertEqual(1234 + 123, card_reading.metadata.response_ms)
        self.assertEqual(2000 + 60, card_reading.metadata.max_tokens)
        self.assertEqual(30 + 50, card_reading.metadata.prompt_tokens)
        self.assertEqual(200 + 5, card_reading.metadata.completion_tokens)
        self.assertEqual(230 + 55, card_reading.metadata.total_tokens)
        self.assertIsNone(card_reading.metadata.temperature)
        self.assertEqual(0.1, card_reading.metadata.top_p)
        self.assertEqual([TarotCard.TheMagician, TarotCard.TheTower], card_reading.spread)
        self.assertEqual(app.spread.prompt, card_reading.prompt)
        self.assertEqual("one fish two fish red fish dead fish", card_reading.response)
        self.assertEqual("Mixed", card_reading.summary)
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
        self.assertTrue(mock_create_spread.called)
        self.assertTrue(mock_interpret_spread.called)
# pylint: enable=C0115,C0116,R0903
