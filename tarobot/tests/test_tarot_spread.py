#!/usr/bin/env python3


import unittest

from tarobot.tarot.tarot_card import TarotCard
from tarobot.tarot.tarot_spread import Spread, SpreadType, SpreadBuilder


class TestTarotSpread(unittest.TestCase):

    def setUp(self) -> None:
        self.spread_builder = SpreadBuilder()

    def test_build_for_one_card(self):
        # Given: a one card tarot spread
        cards = [TarotCard.KingOfPentacles]
        # And:   the type of tarot spread
        spread_type = SpreadType.ONE_CARD

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards)

        # Then:  the expected prompt is generated
        self.assertEqual('Tarot card reading for King of Pentacles.', spread.prompt)

    def test_build_for_card_list_with_seeker_and_teller(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.CARD_LIST_WITH_SEEKER_AND_TELLER
        # And:   some additional parameters for the spread
        parameters = {
            'seeker': 'the seeker',
            'teller': 'Dr Seuss'
        }

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards, parameters)

        # Then:  the expected prompt is generated
        self.assertEqual(('Tarot card reading for the seeker '
                          'with the cards King of Pentacles, Knight of Wands, The Magician '
                          'in the style of Dr Seuss.'), spread.prompt)

    def test_build_for_past_present_future(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.PAST_PRESENT_FUTURE

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards)

        # Then:  the expected prompt is generated
        self.assertEqual(('Tarot card reading with '
                          'King of Pentacles representing the past, '
                          'Knight of Wands representing the present, '
                          'The Magician representing the future.'), spread.prompt)

    def test_build_for_seeker_subject_relationship(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.SEEKER_SUBJECT_RELATIONSHIP

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards)

        # Then:  the expected prompt is generated
        self.assertEqual(('Tarot card reading for love and relationships with '
                          'King of Pentacles representing the seeker, '
                          'Knight of Wands representing the subject, '
                          'The Magician representing the relationship.'), spread.prompt)

    def test_build_for_situation_obstacle_advice(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.SITUATION_OBSTACLE_ADVICE
        # And:   some additional parameters for the spread
        parameters = {
            'situation': 'challenges at work',
            'obstacle': 'difficulties with a co-worker'
        }

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards, parameters)

        # Then:  the expected prompt is generated
        self.assertEqual(('Tarot card reading with '
                          'King of Pentacles representing the situation, '
                          'Knight of Wands representing the obstacle, '
                          'The Magician representing the advice. '
                          'The seeker wants advice about challenges at work. '
                          'The obstacle in their situation is difficulties with a co-worker.'), spread.prompt)
