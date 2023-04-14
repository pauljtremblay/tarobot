#!/usr/bin/env python3

"""Tarot deck cartomancy application.

This module processes command line arguments and executes the desired command.
"""

__all__ = ['CONFIG', 'Config', 'ConfigLoader', 'CommandParser', 'CommandDto', 'App']

from . config import CONFIG, Config, ConfigLoader
from . command_parser import CommandParser, CommandDto
from . app import App
