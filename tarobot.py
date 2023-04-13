#!/usr/bin/env python3

"""Main entry point for the utility from the root directory. Configures the app's logging before running."""

from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO
import sys

from tarobot.app import App


# log levels for different third-party libraries
log_appender_configs = {
    'openai': INFO,
    'urllib3': INFO
}


# NOTE: this should move into external config
def initialize_logging():
    """Initializes the logging framework for the application."""
    # configure root appender for application
    root_logger = getLogger()
    root_logger.setLevel(DEBUG)
    handler = StreamHandler(sys.stdout)
    handler.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    # configure log levels for third party libs
    for logger_name, log_level in log_appender_configs.items():
        getLogger(logger_name).setLevel(log_level)


if __name__ == "__main__":
    initialize_logging()
    app = App()
    app.main()
