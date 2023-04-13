#!/usr/bin/env python3

"""Base test class that sets up an app config fixture for any test classes requiring app config."""

from os.path import dirname, realpath
import unittest

from tests import ConfigLoader


class BaseTestWithConfig(unittest.TestCase):
    """Base class for any unit test classes that use the app's configuration."""

    def setUp(self):
        config_path = realpath(dirname(__file__)) + "/config/test_tarobot.conf"
        self.test_config = ConfigLoader(config_path).config
