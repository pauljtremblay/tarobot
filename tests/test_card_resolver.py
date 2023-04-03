#!/usr/bin/env python3

from tarot import CardResolver, CardValue, Suit, TarotCard
import unittest


class TestCardResolver(unittest.TestCase):

    def setUp(self):
        self.resolver = CardResolver('config/test_aliases.conf')

    def test_get_card_by_alias_happy_path(self):
        # Given: a card's name
        card_name = "TheWorld"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_card_by_alias(card_name)

        # Then:  the expected TarotCard is returned
        self.assertEqual(TarotCard.TheWorld, tarot_card)

    def test_get_card_by_alias_upper(self):
        # Given: a card's name (all uppercase)
        card_name = "THEWORLD"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_card_by_alias(card_name)

        # Then:  the expected TarotCard is returned
        self.assertEqual(TarotCard.TheWorld, tarot_card)

    def test_get_card_by_alias_another_alias(self):
        # Given: a card's alias
        card_name = "THEPOPE"

        # When:  the card is resolved by alias
        tarot_card = self.resolver.get_card_by_alias(card_name)

        # Then:  the expected TarotCard is returned
        self.assertEqual(TarotCard.TheHierophant, tarot_card)

    def test_get_suit_by_alias_happy_path(self):
        # Given: a suit's alias
        suit_name = "Wands"

        # When:  the suit is resolved by alias
        tarot_suit = self.resolver.get_suit_by_alias(suit_name)

        # Then:  the expected Suit is returned
        self.assertEqual(Suit.Wands, tarot_suit)

    def test_get_suit_by_alias_upper(self):
        # Given: a suit's alias
        suit_name = "PENTACLES"

        # When:  the suit is resolved by alias
        tarot_suit = self.resolver.get_suit_by_alias(suit_name)

        # Then:  the expected Suit is returned
        self.assertEqual(Suit.Pentacles, tarot_suit)

    def test_get_suit_by_alias_another_alias(self):
        # Given: a suit's alias
        suit_name = "Discs"

        # When:  the suit is resolved by alias
        tarot_suit = self.resolver.get_suit_by_alias(suit_name)

        # Then:  the expected Suit is returned
        self.assertEqual(Suit.Pentacles, tarot_suit)

    def test_get_rank_by_alias_happy_path(self):
        # Given: a card's rank
        rank_name = "Knight"

        # When:  the card value is resolved by alias
        card_value = self.resolver.get_rank_by_alias(rank_name)

        # Then:  the expected CardValue is returned
        self.assertEqual(CardValue.Knight, card_value)

    def test_get_rank_by_alias_upper(self):
        # Given: a card's rank (in uppercase)
        rank_name = "ACE"

        # When:  the card value is resolved by alias
        card_value = self.resolver.get_rank_by_alias(rank_name)

        # Then:  the expected CardValue is returned
        self.assertEqual(CardValue.Ace, card_value)

    def test_get_rank_by_alias_another_alias(self):
        # Given: a card rank's alias
        rank_name = "Deuce"

        # When:  the card value is resolved by alias
        card_value = self.resolver.get_rank_by_alias(rank_name)

        # Then:  the expected CardValue is returned
        self.assertEqual(CardValue.Two, card_value)

    # TODO find a "generator" way to verify many input -> output combinations
    # check out unittest_data_provider


if __name__ == '__main__':
    unittest.main()
