#!/usr/bin/env python3

import unittest

from tarobot.app import ConfigLoader


class TestWithConfig(unittest.TestCase):
    """Base class for any unit test classes that use the app's configuration."""

    def setUp(self):
        self.test_config = ConfigLoader("config/test_tarobot.conf").config
