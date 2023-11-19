#!/usr/bin/env python3

"""Module containing unit tests around parsing user input from the command line."""

from datetime import datetime
import unittest
from unittest.mock import patch, Mock

from tarobot.app.app import persist_card_reading
from tarobot.db.card_reading_entity import CardReadingEntity
from tarobot.tarot import CardReading, TarotCard


# pylint: disable=C0115,C0116,R0914
class TestCommandParser(unittest.TestCase):

    def test_constructor(self):
        # Given: some mocked up tarot card reading data
        spread = [TarotCard.TheWheelOfFortune, TarotCard.KingOfPentacles, TarotCard.ThreeOfCups]
        prompt = "Tarot card reading for the seeker blah blah blah"
        response = "Yo, good things are gonna come to you"
        summary = "Positive"
        parameters = {
            "subject": "the seeker",
            "teller": "Bob"
        }
        # And:   a mocked up openai Completion response
        completion = Mock()
        completion.id = 'cmpl-444555'
        completion.engine = 'generate'
        completion.model = 'scatgpt-4'
        completion.created = 1681571451
        completion.usage = Mock()
        completion.usage.prompt_tokens = 30
        completion.usage.completion_tokens = 200
        completion.usage.total_tokens = 230

        # When:  the CardReading is constructed from the Completion and card reading attributes
        card_reading = CardReading(completion, spread, prompt, response, parameters, summary)

        # Then:  the attributes are unpacked and stored in the expected fields of CardReading, Metadata DTOs
        self.assertEqual(spread, card_reading.spread)
        self.assertEqual(prompt, card_reading.prompt)
        self.assertEqual(response, card_reading.response)
        self.assertEqual(parameters, card_reading.parameters)
        metadata = card_reading.metadata
        self.assertEqual("cmpl-444555", metadata.openai_id)
        self.assertEqual("scatgpt-4", metadata.model)
        self.assertEqual(1681571451, metadata.created_ts)
        self.assertEqual(30, metadata.prompt_tokens)
        self.assertEqual(200, metadata.completion_tokens)
        self.assertEqual(230, metadata.total_tokens)

    @patch("tarobot.app.app.session_factory")
    def test_persist_card_reading(self, mock_session_factory):
        # Given: a populated CardReading DTO
        card_1 = TarotCard.TheWheelOfFortune
        card_2 = TarotCard.KingOfPentacles
        card_3 = TarotCard.TheFool
        card_4 = TarotCard.TheMagician
        card_5 = TarotCard.TheEmpress
        spread = [card_1, card_2, card_3, card_4, card_5]
        parameters = {
            "subject": "the seeker",
            "teller": "Bob"
        }
        prompt = "Tarot card reading for the seeker blah blah blah"
        response = "Yo, good things are gonna come to you"
        summary = "Positive"
        completion = Mock()
        completion.id = 'cmpl-444555'
        completion.engine = 'generate'
        completion.model = 'scatgpt-4'
        completion.created = 1681571451
        completion.usage = Mock()
        completion.usage.prompt_tokens = 30
        completion.usage.completion_tokens = 200
        completion.usage.total_tokens = 230
        card_reading = CardReading(completion, spread, prompt, response, parameters, summary)
        card_reading.metadata.max_tokens = 2000
        card_reading.metadata.top_p = 0.1

        # When:  the card reading is persisted to the database
        persist_card_reading(card_reading)
        entity: CardReadingEntity
        (entity,) = mock_session_factory.mock_calls[3][1]

        # Then:  the columns are filled in correctly in the intercepted entity
        self.assertEqual(10, entity.card_one)
        self.assertEqual(77, entity.card_two)
        self.assertEqual(0, entity.card_three)
        self.assertEqual(1, entity.card_four)
        self.assertEqual(3, entity.card_five)
        self.assertEqual('{"subject": "the seeker", "teller": "Bob"}', entity.parameters)
        self.assertEqual("Tarot card reading for the seeker blah blah blah", entity.prompt)
        self.assertEqual("Yo, good things are gonna come to you", entity.response)
        self.assertEqual("Positive", entity.summary)
        self.assertEqual("cmpl-444555", entity.openai_id)
        self.assertEqual("scatgpt-4", entity.model)
        self.assertEqual(datetime.fromtimestamp(1681571451), entity.created_ts)
        self.assertEqual(2000, entity.max_tokens)
        self.assertEqual(30, entity.prompt_tokens)
        self.assertEqual(200, entity.completion_tokens)
        self.assertEqual(230, entity.total_tokens)
        self.assertIsNone(entity.temperature)
        self.assertEqual(0.1, entity.top_p)
# pylint: disable=C0115,C0116,R0914
