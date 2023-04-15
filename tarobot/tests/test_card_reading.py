#!/usr/bin/env python3

"""Module containing unit tests around parsing user input from the command line."""

import unittest

from openai import Completion

from tarobot.tarot import CardReading, TarotCard


# pylint: disable=C0115,C0116
class TestCommandParser(unittest.TestCase):

    def test_constructor(self):
        # Given: some mocked up tarot card reading data
        spread = [TarotCard.TheWheelOfFortune, TarotCard.KingOfPentacles, TarotCard.ThreeOfCups]
        prompt = "Tarot card reading for the seeker blah blah blah"
        response = "Yo, good things are gonna come to you"
        subject = "the seeker"
        teller = "Bob"
        # And:   a mocked up openai Completion response
        completion = Completion(id='cmpl-444555',
                                engine='generate',
                                response_ms=1234)
        completion['model'] = 'scatgpt-4'
        completion['created'] = 1681571451
        completion['usage'] = {'prompt_tokens': 30, 'completion_tokens': 200, 'total_tokens': 230}

        # When:  the CardReading is constructed from the Completion and card reading attributes
        card_reading = CardReading(completion, spread, prompt, response, subject, teller)

        # Then:  the attributes are unpacked and stored in the expected fields of CardReading, Metadata DTOs
        self.assertEqual(spread, card_reading.spread)
        self.assertEqual(prompt, card_reading.prompt)
        self.assertEqual(response, card_reading.response)
        self.assertEqual(subject, card_reading.subject)
        self.assertEqual(teller, card_reading.teller)
        metadata = card_reading.metadata
        self.assertEqual("cmpl-444555", metadata.openai_id)
        self.assertEqual("scatgpt-4", metadata.model)
        self.assertEqual(1681571451, metadata.created_ts)
        self.assertEqual(1234, metadata.response_ms)
        self.assertEqual(30, metadata.prompt_tokens)
        self.assertEqual(200, metadata.completion_tokens)
        self.assertEqual(230, metadata.total_tokens)
# pylint: disable=C0115,C0116
