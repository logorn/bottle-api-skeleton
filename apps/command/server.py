#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

import logging
import logging.config
import argparse

from apps.settings import Settings, __version__
from ..bootstrap import bootstrap

class Server():
    def __init__(self):
        """Class instantiation.

        Initialize arguments and options
        """
        self.parser = argparse.ArgumentParser(description=self.__doc__)
        self.parser.add_argument(
            "-c",
            "--config",
            type=str,
            metavar="CONFIG",
            default="local",
            help="configuration file (default: %(default)s)"
        )
        self.parser.add_argument(
            "-v",
            "--version",
            action='version',
            version='%(prog)s ' + __version__
        )

        self.logger = logging.getLogger()

    def main(self):
        """Run the command
        * Retrieve options sent by user.
        * Launche app
        """
        options = self.parser.parse_args()
        settings = Settings(options.config)
        logging.config.dictConfig(settings.LOGGING)
        bootstrap().main()

def main():
    """Main function to run command. Used by console_scripts entry point
    """
    Server().main()

if __name__ == '__main__':
   main()