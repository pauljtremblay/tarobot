#!/usr/bin/env python3

import unittest
from tarot import *

CARDS_IN_DECK = 78


class TestTarot(unittest.TestCase):

    def test_deck_is_complete(self):
        # When:  a tarot deck is instantiated
        deck = TarotDeck()

        # Then:  all 78 cards are present in the deck
        self.assertEqual(len(deck.cards), CARDS_IN_DECK)
        for ordinal in range(0, CARDS_IN_DECK):
            found = False
            for card in deck.cards:
                if card.value == ordinal:
                    found = True
                    break
            self.assertTrue(found, msg="card with ordinal value %i is missing from deck" % ordinal)

    def test_deck_is_shuffled(self):
        # When:  a tarot deck is instantiated
        deck = TarotDeck()

        # Then:  the cards have been shuffled
        ordered = True
        for ordinal in range(0, CARDS_IN_DECK):
            if deck.cards[ordinal].value != ordinal:
                ordered = False
                break
        self.assertFalse(ordered, msg="tarot deck is in perfect order")

    def test_dealt_card_is_removed(self):
        # Given: a shuffled tarot deck
        deck = TarotDeck()

        # When:  a card is drawn from the deck
        (drawn_card) = deck.draw(1)

        # Then:  the drawn card is no longer present in the deck
        self.assertEqual(len(deck.cards), CARDS_IN_DECK - 1)
        self.assertNotIn(drawn_card, deck.cards)

    def test_major_archana_card_by_ordinal(self):
        # When:  an arbitrary major archana card is specified by its ordinal value
        major_card = TarotCard(1)

        # Then:  the expected card is retrieved
        self.assertEqual(major_card, TarotCard.TheMagician)
        # And:   the expected card properties exist
        self.assertEqual(major_card.value, 1)
        self.assertEqual(major_card.archana(), Archana.Major)
        self.assertEqual(major_card.suit(), None)
        self.assertEqual(major_card.card_value(), None)
        # And:    the string representation is human-readable
        self.assertEqual(str(major_card), "The Magician")

    def test_minor_archana_card_by_ordinal(self):
        # When:  an arbitrary minor archana card is specified by its ordinal value
        minor_card = TarotCard(55)

        # Then:  the expected card is retrieved
        self.assertEqual(minor_card, TarotCard.SixOfSwords)
        # And:   the expected card properties exist
        self.assertEqual(minor_card.value, 55)
        self.assertEqual(minor_card.archana(), Archana.Minor)
        self.assertEqual(minor_card.suit(), Suit.Swords)
        self.assertEqual(minor_card.card_value(), CardValue.Six)
        # And:    the string representation is human-readable
        self.assertEqual(str(minor_card), "Six of Swords")

    def test_card_by_name(self):
        # When:  an arbitrary card is specified by its proper name
        card = TarotCard.TheMagician

        # Then:  the expected card properties exist
        self.assertEqual(card.value, 1)
        self.assertEqual(card.archana(), Archana.Major)
        self.assertEqual(card.suit(), None)
        self.assertEqual(card.card_value(), None)
        # And:    the string representation is human-readable
        self.assertEqual(str(card), "The Magician")


if __name__ == '__main__':
    unittest.main()
