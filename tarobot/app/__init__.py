#!/usr/bin/env python3

"""Tarot deck cartomancy application.

This module processes command line arguments and executes the desired command.
"""

__all__ = ['App', 'CommandParser', 'CommandDto', 'config', 'Config', 'ConfigLoader']

from tarobot.app.config import config, Config, ConfigLoader
from tarobot.app.command_parser import CommandParser, CommandDto
from tarobot.app.app import App
