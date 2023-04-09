#!/usr/bin/env python3

from app import ConfigLoader
import unittest


class TestWithConfig(unittest.TestCase):
    """Base class for any unit test classes that use the app's configuration."""

    def setUp(self):
        self.test_config = ConfigLoader("config/test_tarobot.conf").config
