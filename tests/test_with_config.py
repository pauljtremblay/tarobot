#!/usr/bin/env python3

from app import ConfigLoader
from tarot import CardResolver
import unittest


class TestWithConfig(unittest.TestCase):
    """Base class for any unit test classes that use the app's configuration."""

    def setUp(self):
        self.config = ConfigLoader("config/test_tarobot.conf").config
        self.resolver = CardResolver("config/test_aliases.conf")
