#!/usr/bin/env python3

from app import ConfigLoader
import unittest


class TestConfig(unittest.TestCase):

    def test_config_loader(self):
        # Given: a config file to load
        config_path = 'config/test_tarobot.conf'

        # When:  the config is loaded
        loader = ConfigLoader(config_path)

        # Then:  the configuration is loaded into the data classes
        conf = loader.config
        self.assertIsNotNone(conf.app_name)
        # And:   the openai configuration is set
        self.assertIsNotNone(conf.openai.api_key)
        self.assertIsNotNone(conf.openai.completion)
        # And:   the tarot card spread rules are logically consistent
        self.assertGreaterEqual(conf.tarot.min_cards, 1)
        self.assertGreaterEqual(conf.tarot.max_cards, conf.tarot.min_cards)
        self.assertGreaterEqual(conf.tarot.default_cards, conf.tarot.min_cards)
        self.assertGreaterEqual(conf.tarot.max_cards, conf.tarot.default_cards)


if __name__ == '__main__':
    unittest.main()
