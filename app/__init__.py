#!/usr/bin/env python3

"""Tarot deck cartomancy application.

This module processes command line arguments and executes the desired command.
"""

__all__ = ['App', 'CommandParser', 'CommandDto', 'Config', 'ConfigLoader']

from app.app import App
from app.command_parser import CommandParser, CommandDto
from app.config import Config, ConfigLoader
