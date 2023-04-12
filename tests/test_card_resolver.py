#!/usr/bin/env python3

from os.path import dirname, realpath
import unittest

from tarobot.tarot import CardResolver, CardValue, Suit, TarotCard


class TestCardResolver(unittest.TestCase):

    def setUp(self):
        config_path = realpath(dirname(__file__)) + '/config/test_aliases.conf'
        self.resolver = CardResolver(config_path)

    def test_get_card_by_known_alias_happy_path(self):
        # Given: a card's name
        card_name = "TheWorld"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_card_by_known_alias(card_name)

        # Then:  the expected TarotCard is returned
        self.assertEqual(TarotCard.TheWorld, tarot_card)

    def test_get_card_by_known_alias_upper(self):
        # Given: a card's name (all uppercase)
        card_name = "THEWORLD"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_card_by_known_alias(card_name)

        # Then:  the expected TarotCard is returned
        self.assertEqual(TarotCard.TheWorld, tarot_card)

    def test_get_card_by_known_alias_another_alias(self):
        # Given: a card's alias
        card_name = "The POPE"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_card_by_known_alias(card_name)

        # Then:  the expected TarotCard is returned
        self.assertEqual(TarotCard.TheHierophant, tarot_card)

    def test_get_suit_by_known_alias_happy_path(self):
        # Given: a suit's alias
        suit_name = "Wands"

        # When:  the suit is resolved by alias
        tarot_suit = self.resolver.get_suit_by_known_alias(suit_name)

        # Then:  the expected Suit is returned
        self.assertEqual(Suit.Wands, tarot_suit)

    def test_get_suit_by_known_alias_upper(self):
        # Given: a suit's alias
        suit_name = "PENTACLES"

        # When:  the suit is resolved by alias
        tarot_suit = self.resolver.get_suit_by_known_alias(suit_name)

        # Then:  the expected Suit is returned
        self.assertEqual(Suit.Pentacles, tarot_suit)

    def test_get_suit_by_known_alias_another_alias(self):
        # Given: a suit's alias
        suit_name = "Discs"

        # When:  the suit is resolved by alias
        tarot_suit = self.resolver.get_suit_by_known_alias(suit_name)

        # Then:  the expected Suit is returned
        self.assertEqual(Suit.Pentacles, tarot_suit)

    def test_get_rank_by_known_alias_happy_path(self):
        # Given: a card's rank
        rank_name = "Knight"

        # When:  the card value is resolved by alias
        card_value = self.resolver.get_rank_by_known_alias(rank_name)

        # Then:  the expected CardValue is returned
        self.assertEqual(CardValue.Knight, card_value)

    def test_get_rank_by_known_alias_upper(self):
        # Given: a card's rank (in uppercase)
        rank_name = "ACE"

        # When:  the card value is resolved by alias
        card_value = self.resolver.get_rank_by_known_alias(rank_name)

        # Then:  the expected CardValue is returned
        self.assertEqual(CardValue.Ace, card_value)

    def test_get_rank_by_known_alias_another_alias(self):
        # Given: a card rank's alias
        rank_name = "Deuce"

        # When:  the card value is resolved by alias
        card_value = self.resolver.get_rank_by_known_alias(rank_name)

        # Then:  the expected CardValue is returned
        self.assertEqual(CardValue.Two, card_value)

    # TODO find a "generator" way to verify many input -> output combinations
    # check out unittest_data_provider

    def test_get_optional_card_by_alias_happy_path(self):
        # Given: a known card's alias
        card_name = "FiveOfSwords"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_optional_card_by_alias(card_name)

        # Then:  expected CardValue is returned
        self.assertEqual(TarotCard.FiveOfSwords, tarot_card)

    def test_get_optional_card_by_alias_still_resolvable(self):
        # Given: a previously unknown card alias
        card_name = "DeuceOfCoins"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_optional_card_by_alias(card_name)

        # Then:  expected CardValue is returned
        self.assertEqual(TarotCard.TwoOfPentacles, tarot_card)

    def test_get_optional_card_by_alias_unresolvable(self):
        # Given: an unresolvable tarot card alias
        card_name = "FooOfBar"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_optional_card_by_alias(card_name)

        # Then:  no matching TarotCard is found
        self.assertIsNone(tarot_card)


if __name__ == '__main__':
    unittest.main()
