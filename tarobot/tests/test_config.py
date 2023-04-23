#!/usr/bin/env python3

"""Module containing unit tests around the application's config loading logic."""

from os.path import dirname, realpath
import unittest

from tarobot.app import ConfigLoader


# pylint: disable=C0115,C0116
class TestConfig(unittest.TestCase):

    def test_config_loader(self):
        # Given: a config file to load
        config_path = realpath(dirname(__file__)) + '/config/test_tarobot.conf'

        # When:  the config is loaded
        loader = ConfigLoader(config_path)

        # Then:  the configuration is loaded into the data classes
        config = loader.config
        self.assertIsNotNone(config.app_name)
        # And:   the openai configuration is set
        self.assertIsNotNone(config.openai.api_key)
        self.assertIsNotNone(config.openai.generate_reading)
        self.assertIsNotNone(config.openai.summarize_reading)
        # And:   the persistence layer settings are present
        self.assertIsNotNone(config.db)
        # And:   the tarot card spread rules are logically consistent
        self.assertGreaterEqual(config.tarot.min_cards, 1)
        self.assertGreaterEqual(config.tarot.max_cards, config.tarot.min_cards)
        self.assertGreaterEqual(config.tarot.default_cards, config.tarot.min_cards)
        self.assertGreaterEqual(config.tarot.max_cards, config.tarot.default_cards)
# pylint: enable=C0115,C0116
