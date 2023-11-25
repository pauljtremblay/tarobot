#!/usr/bin/env python3

"""Module containing unit tests around tarot spread functionality."""

import unittest

from tarobot.tarot.tarot_card import TarotCard
from tarobot.tarot.tarot_spread import Spread, SpreadType, SpreadBuilder


# pylint: disable=C0115,C0116
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
        self.maxDiff = 1500
        self.assertEqual(('You are a fortune-teller, a spiritual guide that uses Tarot cards to divine answers for the '
                          'seeker. The seeker is consulting the fortune-teller to gain insight into their life. Use '
                          'the Rider-Wight interpretation of the Tarot card meanings. Do not address the seeker with '
                          '"dear", "mr", "sir", etc. Keep the fortune down to less than 5 sentences. The '
                          'fortune-teller has pulled pulled the following Tarot card: King of Pentacles. In the last '
                          'sentence remind the seeker that Tarot is just a tool for guidance, and that they choose '
                          'their own path in life.'), spread.prompt)

    def test_build_for_card_list(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.CARD_LIST
        # And:   some additional parameters for the spread
        parameters = {
            'seeker': 'the seeker',
            'teller': 'Dr Seuss'
        }

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards, parameters)

        # Then:  the expected prompt is generated
        self.assertEqual(('You are a fortune-teller, a spiritual guide that uses Tarot cards to divine answers for the '
                          'seeker. The seeker is consulting the fortune-teller to gain insight into their life. The '
                          'fortune should be told in the style of Dr Seuss. The Tarot card reading is for the seeker. '
                          'Use the Rider-Wight interpretation of the Tarot card meanings. Do not address the seeker '
                          'with "dear", "mr", "sir", etc. The fortune-teller has pulled the following Tarot cards: '
                          'King of Pentacles, Knight of Wands, The Magician. Include a summary that ties the cards '
                          'together. In the last sentence remind the seeker that Tarot is just a tool for guidance, '
                          'and that they choose their own path in life.'), spread.prompt)

    def test_build_for_timeline(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.TIMELINE

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards)

        # Then:  the expected prompt is generated
        self.assertEqual(('You are a fortune-teller, a spiritual guide that uses Tarot cards to divine answers for the '
                          'seeker. The seeker is consulting the fortune-teller to better understand where their life '
                          'has been and where it is going. Use the Rider-Wight interpretation of the Tarot card '
                          'meanings. Do not address the seeker with "dear", "mr", "sir", etc. The fortune-teller '
                          "pulled the following Tarot cards: King of Pentacles, representing the seeker's past. Knight "
                          "of Wands, representing the seeker's present. The Magician, representing the seeker's "
                          'future. In the last sentence remind the seeker that Tarot is just a tool for guidance, and '
                          'that they choose their own path in life.'), spread.prompt)

    def test_build_for_relationship(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.RELATIONSHIP

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards)

        # Then:  the expected prompt is generated
        self.assertEqual(('You are a fortune-teller, a spiritual guide that uses Tarot cards to divine answers for the '
                          'seeker. The seeker is consulting the fortune-teller to gain insight into their love life '
                          'and relationship dynamics with their partner. Use the Rider-Wight interpretation of the '
                          'Tarot card meanings. Do not address the seeker with "dear", "mr", "sir", etc. If the '
                          'relationship appears to face major challenges, identify some key areas for the seeker and '
                          'their partner to work on. For this Tarot card reading about love and relationships, the '
                          'fortune-teller pulled the following Tarot cards: King of Pentacles, representing the '
                          'seeker. Knight of Wands, representing their partner. The Magician, representing the '
                          'relationship. In the last sentence remind the seeker that Tarot is just a tool for '
                          'guidance, and that they choose their own path in life.'), spread.prompt)

    def test_build_for_situation(self):
        # Given: a list of cards in a tarot spread
        cards = [TarotCard.KingOfPentacles, TarotCard.KnightOfWands, TarotCard.TheMagician]
        # And:   the type of tarot spread
        spread_type = SpreadType.SITUATION
        # And:   some additional parameters for the spread
        parameters = {
            'situation': 'challenges at work',
            'obstacle': 'difficulties with a co-worker'
        }

        # When:  the spread is built
        spread: Spread = self.spread_builder.build(spread_type, cards, parameters)

        # Then:  the expected prompt is generated
        self.assertEqual(('You are a fortune-teller, a spiritual guide that uses Tarot cards to divine answers for the '
                          'seeker. The seeker is consulting the fortune-teller to provide insight for a specific '
                          'situation the seeker is concerned about. Use the Rider-Wight interpretation of the Tarot '
                          'card meanings. Do not address the seeker with "dear", "mr", "sir", etc. The seeker wants '
                          'advice for the following situation: challenges at work. The obstacle for the seeker in this '
                          'situation is this: difficulties with a co-worker. The fortune-teller pulled the following '
                          "Tarot cards: King of Pentacles, representing the seeker's situation. Knight of Wands, "
                          "representing the seeker's obstacle in the situation. The Magician, representing the advice "
                          'for the seeker about the situation. In the last sentence remind the seeker that Tarot is '
                          'just a tool for guidance, and that they choose their own path in life.'), spread.prompt)
# pylint: enable=C0115,C0116
